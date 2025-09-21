# 🛒 Shopee Product Scraper (Apify + Python)
# Crawling Data Shopee Youtube (Tutorial) : https://youtu.be/oAzTbsH-58I?si=FSW0cY8GSpUUDbYu

Project ini adalah **scraper produk Shopee** menggunakan [Apify Actor](https://apify.com) dan Python.  
Tujuannya untuk mengambil data produk seperti **nama, harga, stok, rating, kategori, gambar, dan lokasi pengiriman** lalu menyimpannya ke format **Excel** untuk analisis lebih lanjut.  

## ✨ Fitur
- Ambil data produk langsung dari **link Shopee**.
- Ekstraksi detail produk:
  - Nama produk
  - Deskripsi
  - Harga normal, harga terendah & tertinggi
  - Stok
  - Rating & total ulasan
  - Kategori produk
  - Gambar utama & sub-gambar
  - Lokasi pengiriman
- Simpan hasil ke **Excel (.xlsx)**.
- Cetak hasil juga dalam format **JSON**.

## 📦 Requirements
- Python 3.8+
- [Apify Account](https://apify.com) + API Token
- Library Python:
  - `apify_client`
  - `pandas`

Install dependencies:
```bash
pip install apify-client pandas
