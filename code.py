import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

def fetch_weather(city):
    API_key = "5c2c65a670c2ff85c2ec754b59f35eeb"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    response = requests.get(url)

    if response.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    weather_data = response.json()

    if 'weather' not in weather_data or 'main' not in weather_data or 'sys' not in weather_data or 'name' not in weather_data:
        messagebox.showerror("Error", "Invalid weather data")
        return None

    weather_icon_id = weather_data['weather'][0]['icon']
    temperature = weather_data['main']['temp'] - 273.15
    description = weather_data['weather'][0]['description']
    city_name = weather_data['name']
    country = weather_data['sys']['country']

    weather_icon_url = f"http://openweathermap.org/img/wn/{weather_icon_id}@2x.png"
    return (weather_icon_url, temperature, description, city_name, country)

def search_weather():
    city = city_entry.get()
    weather_info = fetch_weather(city)
    if weather_info is None:
        return

    weather_icon_url, temperature, description, city_name, country = weather_info
    location_label.configure(text=f"{city_name}, {country}", fg="yellow")

    image_data = requests.get(weather_icon_url).content
    weather_icon = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    icon_label.configure(image=weather_icon)
    icon_label.image = weather_icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C", fg="orange")
    description_label.configure(text=f"Description: {description}", fg="green")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="grey")

city_entry = tk.Entry(root, font="Arial, 18")
city_entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=search_weather, bg="yellow", fg="grey")
search_button.pack(pady=10)

location_label = tk.Label(root, font="Arial, 25", fg="yellow", bg="grey")
location_label.pack(pady=20)

icon_label = tk.Label(root, bg="grey")
icon_label.pack()

temperature_label = tk.Label(root, font="Arial, 20", fg="orange", bg="grey")
temperature_label.pack()

description_label = tk.Label(root, font="Arial, 20", fg="green", bg="grey")
description_label.pack()

root.mainloop()
