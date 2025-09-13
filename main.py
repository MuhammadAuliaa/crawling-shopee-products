from apify_client import ApifyClient
import json
import pandas as pd

# Initialize the ApifyClient with your API token
client = ApifyClient("")

# prepare the list of product URLs to scrape
product_urls = [
    "https://shopee.co.id/Sony-Alpha-a6400-a-6400-Mirrorless-Digital-Camera-with-E-PZ-16-50mm-f3.5-5.6-OSS-II-i.107010302.3603033395?sp_atk=ce7bf5ba-55d7-4652-a5be-7a2abc1817e9&xptdk=ce7bf5ba-55d7-4652-a5be-7a2abc1817e9",
    "https://shopee.co.id/Hollyland-Lark-A1-Wireless-Microphone-Smartphone-Android-iPhone-iPad-Action-Camera-Laptop-i.289594870.29186074543?sp_atk=c2be0660-2aac-47ef-82e6-a0477176c676&xptdk=c2be0660-2aac-47ef-82e6-a0477176c676",
    "https://shopee.co.id/Apple-MacBook-Pro-M4-Pro-Max-14-Inch-1TB-512GB-SSD-RAM-36GB-24GB-i.304902524.25688260631?sp_atk=20f3f408-1c91-4c42-a762-6a1c86e6c38a&xptdk=20f3f408-1c91-4c42-a762-6a1c86e6c38a",
    "https://shopee.co.id/Bodypack-Shilka-Vision-1.0-Laptop-Backpack-14-Inch-Tas-Ransel-Kerja-Kuliah-Sekolah-Ringan-Multifungsi-17-L-Hitam-i.217842108.22758396887?sp_atk=1a2d90bc-b574-4f0e-9b1b-279f229e5d39&xptdk=1a2d90bc-b574-4f0e-9b1b-279f229e5d39",
    "https://shopee.co.id/Siap-INBEX-Softball-Professional-Softbox-Photography-Studio-Portrait-Video-live-pembuatan-konten-i.1090906161.26001253990?sp_atk=7bc39742-60a7-47fd-8029-69c80049d842&xptdk=7bc39742-60a7-47fd-8029-69c80049d842",
    "https://shopee.co.id/KUCADI-Dumbbell-Set-20kg-30-kg-40-kg-Peralatan-Fitness-Barbel-Set-Dengan-Perlindungan-Lingkungan-Garansi-lima-tahun--i.1304933658.29455164577?sp_atk=ef861ef5-b695-4142-b2f5-440337799765&xptdk=ef861ef5-b695-4142-b2f5-440337799765",
    "https://shopee.co.id/Apple-iPhone-13-i.255563049.13342260145?sp_atk=04331e6a-5d42-41dc-80d0-8f08d68fc7d0&xptdk=04331e6a-5d42-41dc-80d0-8f08d68fc7d0",
    "https://shopee.co.id/Pelilit-Kabel-Spiral-Pelindung-Kabel-Charger-Pelindung-Cable-HP-Universal-i.893010372.15199370878?sp_atk=432993a5-2b13-463f-ae13-218a0baee4a8&xptdk=432993a5-2b13-463f-ae13-218a0baee4a8",
    "https://shopee.co.id/Thesilversky-Workshirt-Kemeja-Pendek-Polos-Pria-Premium-i.7966233.24840718855?sp_atk=e42bbf0b-51fa-423d-82d4-b0725daa89f0&xptdk=e42bbf0b-51fa-423d-82d4-b0725daa89f0",
    "https://shopee.co.id/Mac-Mini-M4-M4-Pro-2024-512GB-256GB-16-Core-GPU-RAM-24GB-i.1313789708.27768388924?sp_atk=92dd0245-1dcb-48e2-8414-2a1fb4fbddbb&xptdk=92dd0245-1dcb-48e2-8414-2a1fb4fbddbb"
]

run_input = {"urls": [{"url": link} for link in product_urls]}

# Run the Actor and wait for it to finish
run = client.actor("VKHHxsmZOsISRINnY").call(run_input=run_input)
results = []

# Ambil hasil scraping
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    data = item.get("data", {})
    prod = data.get("item", {})
    review = data.get("product_review", {})
    shipping = data.get("product_shipping", {}).get("shipping_fee_info", {})

    # Gambar utama & tambahan
    main_img = f"https://down-id.img.susercontent.com/file/{prod['image']}" if prod.get("image") else None
    tier_imgs = [
        f"https://down-id.img.susercontent.com/file/{img}"
        for t in prod.get("tier_variations", [])
        for img in (t.get("images") or []) if img
    ]

    # Kategori
    categories = [c["display_name"] for c in prod.get("categories", []) if c.get("display_name")]

    results.append({
        "id_produk": prod.get("item_id"),
        "nama_produk": prod.get("title"),
        "url": item.get("url"),
        "deskripsi": prod.get("description"),
        "harga": prod.get("price", 0) // 100000,
        "harga_terendah": prod.get("price_min", 0) // 100000,
        "harga_tertinggi": prod.get("price_max", 0) // 100000,
        "stok": prod.get("max_quantity"),
        "rating": review.get("rating_star"),
        "total_ulasan": review.get("total_rating_count"),
        "kategori": categories,
        "gambar_produk": main_img,
        "sub_gambar_produk": tier_imgs,
        "lokasi_pengiriman": shipping.get("ship_from_location")
    })

# Simpan ke Excel
df = pd.DataFrame(results)
df.to_excel("shopee_products.xlsx", index=False)

# Cetak dalam format JSON
print(json.dumps(results, indent=2, ensure_ascii=False))