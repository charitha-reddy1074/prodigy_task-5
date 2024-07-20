import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import csv

class MyntraScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Myntra Product Scraper")
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # URL entry
        self.url_label = ttk.Label(self.main_frame, text="Enter Myntra URL:")
        self.url_label.grid(row=0, column=0, sticky="w", pady=10)
        
        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Scrape button
        self.scrape_button = ttk.Button(self.main_frame, text="Scrape", command=self.scrape_and_save)
        self.scrape_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="", foreground="green")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)
        
    def scrape_and_save(self):
        url = self.url_entry.get()
        if url:
            try:
                names, prices, ratings = self.scrape_myntra(url)
                self.save_to_csv((names, prices, ratings), 'myntra_products.csv')
                self.status_label.config(text=f"Scraped {len(names)} products. Data saved to 'myntra_products.csv'.", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                self.status_label.config(text="Error occurred during scraping.", foreground="red")
        else:
            messagebox.showwarning("Warning", "Please enter a Myntra URL.")

    def scrape_myntra(self, url):
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Initialize lists to store data
        product_names = []
        product_prices = []
        product_ratings = []
        
        # Example: Scraping product names, prices, and ratings
        products = soup.find_all('div', class_='product-productMetaInfo')
        
        for product in products:
            # Extract product name
            name = product.find('h3', class_='product-brand').text.strip()
            product_names.append(name)
            
            # Extract product price
            price = product.find('span', class_='product-discountedPrice').text.strip()
            product_prices.append(price)
            
            # Extract product rating
            rating = product.find('div', class_='product-ratingCount').text.strip()
            product_ratings.append(rating)
        
        return product_names, product_prices, product_ratings

    def save_to_csv(self, data, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Rating'])  # Header row
            for item in zip(*data):
                writer.writerow(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyntraScraperApp(root)
    root.mainloop()
