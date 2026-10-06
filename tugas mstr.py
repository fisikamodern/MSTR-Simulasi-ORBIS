import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# ==========================================
# 1. SETUP KANVAS (Hanya Visualisasi Alat)
# ==========================================
fig, ax = plt.subplots(figsize=(14, 7))
fig.canvas.manager.set_window_title('Simulasi Detail ORBIS (Fokus Mekanis)')
ax.set_xlim(0, 16)
# Memperlebar sumbu Y agar teks di atas dan bawah tidak bertumpuk dengan gambar
ax.set_ylim(-1, 8) 
ax.axis('off')

# Judul Utama
ax.text(8, 7.5, "SISTEM TERINTEGRASI ORBIS:\nINCINERATOR, WET SCRUBBER & BIOFILTER MIKROALGA", 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#333333')
ax.text(8, 6.8, ' Data Sensor Terhubung ke ESP32 & Cloud', ha='center', color='#1565C0', fontweight='bold', fontsize=10)

# ==========================================
# 2. MENGGAMBAR DETAIL DESAIN ALAT
# ==========================================
# A. Unit 1: Incinerator
ax.add_patch(patches.Rectangle((0.5, 0.5), 2.5, 3.5, facecolor='#424242', edgecolor='black', lw=2))
ax.add_patch(patches.Rectangle((1.0, 1.0), 1.5, 1.5, facecolor='#FF5722', alpha=0.8)) # Api
ax.text(1.75, 4.3, 'UNIT 1:\nINCINERATOR', ha='center', fontweight='bold', fontsize=10)
ax.text(1.75, 1.75, 'API', ha='center', va='center', fontsize=20, color='white', fontweight='bold')

# B. Unit 2: Wet Scrubber (Filtrasi Kimia)
ax.add_patch(patches.Rectangle((5.0, 0.5), 3.0, 5.0, facecolor='#E3F2FD', edgecolor='#1976D2', lw=2))
# Air Tampungan Limbah
ax.add_patch(patches.Rectangle((5.0, 0.5), 3.0, 1.0, facecolor='#1976D2', alpha=0.6)) 
# Media Packing (Bentuk Grid)
ax.add_patch(patches.Rectangle((5.1, 2.0), 2.8, 1.2, facecolor='none', edgecolor='#607D8B', hatch='xx', lw=1.5)) 
# Nozzle Spray
ax.scatter([6.0, 7.0], [4.8, 4.8], marker='v', color='blue', s=100) 
# Label Wet Scrubber
ax.text(6.5, 5.8, 'UNIT 2: WET SCRUBBER\nMedia Packing & Nozzle Spray', ha='center', fontweight='bold', fontsize=10)
ax.text(6.5, -0.3, '(Larutan NaOH + Kapur Dolomit + POC)', ha='center', fontsize=9, color='#1976D2')

# C. Unit 3: Biofilter Mikroalga
ax.add_patch(patches.Rectangle((10.5, 0.5), 3.0, 5.0, facecolor='#E8F5E9', edgecolor='#388E3C', lw=2))
# Kultur Chlorella vulgaris
ax.add_patch(patches.Rectangle((10.5, 0.5), 3.0, 4.5, facecolor='#4CAF50', alpha=0.6)) 
# LED Grow Light (Garis Kuning di pinggir)
ax.add_patch(patches.Rectangle((10.3, 0.5), 0.1, 4.5, facecolor='#FFEB3B')) 
ax.add_patch(patches.Rectangle((13.6, 0.5), 0.1, 4.5, facecolor='#FFEB3B')) 
# Label Biofilter
ax.text(12.0, 5.8, 'UNIT 3: BIOFILTER\nKultur Chlorella vulgaris', ha='center', fontweight='bold', fontsize=10)
ax.text(12.0, -0.3, 'Dilengkapi LED Grow Light & Aerator', ha='center', fontsize=9, color='#388E3C')

# D. Pipa Gas (Visual Statis)
ax.plot([3.0, 5.0], [3.5, 3.5], color='#9E9E9E', lw=14, solid_capstyle='butt', zorder=0)
ax.plot([8.0, 10.5], [3.5, 3.5], color='#9E9E9E', lw=14, solid_capstyle='butt', zorder=0)
ax.plot([13.5, 15.5], [4.5, 4.5], color='#9E9E9E', lw=14, solid_capstyle='butt', zorder=0)

# E. Menggambar Modul Sensor 3 Titik
sensor_coords = [(4.0, 3.5), (9.25, 3.5), (14.5, 4.5)]
for i, (sx, sy) in enumerate(sensor_coords):
    # Kotak sensor digeser sedikit ke atas pipa
    ax.add_patch(patches.Rectangle((sx-0.5, sy+0.2), 1.0, 0.8, facecolor='#ECEFF1', edgecolor='black', lw=1))
    ax.text(sx, sy+1.3, f'Titik {i+1}', ha='center', color='red', fontweight='bold', fontsize=10)

# F. Legenda Partikel (Ditempatkan di pojok agar rapi)
ax.scatter([], [], color='black', s=50, label='PM2.5 / PM10 (Partikulat)')
ax.scatter([], [], color='orange', s=50, label='CO2 (Karbondioksida)')
ax.scatter([], [], color='cyan', s=50, label='O2 (Oksigen Bersih)')
ax.legend(loc='upper right', fontsize=10, framealpha=0.9, bbox_to_anchor=(1.0, 1.0))

# ==========================================
# 3. INISIALISASI VARIABEL PARTIKEL & EFEK
# ==========================================
scatter_pm = ax.scatter([], [], color='black', s=40, zorder=4)
scatter_co2 = ax.scatter([], [], color='orange', s=50, zorder=4)
scatter_o2 = ax.scatter([], [], color='cyan', s=50, zorder=4)
scatter_water = ax.scatter([], [], color='blue', marker='|', s=60, alpha=0.5, zorder=3)
scatter_bubbles = ax.scatter([], [], facecolor='none', edgecolor='white', s=30, alpha=0.7, zorder=3)

particles = []
water_drops = []
bubbles = []

# ==========================================
# 4. LOGIKA PERGERAKAN ANIMASI
# ==========================================
def update(frame):
    global particles, water_drops, bubbles
    
    # Generate polutan dari tungku pembakaran (Setiap 2 frame)
    if frame % 2 == 0:
        for _ in range(3): particles.append([2.8, 3.5 + np.random.uniform(-0.15, 0.15), 0])
        for _ in range(4): particles.append([2.8, 3.5 + np.random.uniform(-0.15, 0.15), 1])

    # Generate efek lingkungan (Hujan Scrubber & Gelembung Aerator)
    if frame % 2 == 0:
        for _ in range(4): water_drops.append([np.random.uniform(5.2, 7.8), 4.8])
        for _ in range(4): bubbles.append([np.random.uniform(10.7, 13.3), 0.8])

    surviving_particles = []

    for p in particles:
        p[0] += 0.15 # Kecepatan gas bergerak ke kanan
        
        # Dinamika ketinggian partikel (Y)
        if p[0] < 5.0 or (8.0 < p[0] < 10.5) or p[0] > 13.5:
            # Gas terfokus di dalam saluran pipa
            target_y = 4.5 if p[0] > 13.5 else 3.5
            p[1] += np.random.uniform(-0.05, 0.05)
            p[1] = np.clip(p[1], target_y - 0.2, target_y + 0.2)
        else:
            # Gas menyebar saat memasuki tabung reaktor lebar
            p[1] += np.random.uniform(-0.15, 0.15)
            p[1] = np.clip(p[1], 1.5, 4.0)

        # Proses Filtrasi Wet Scrubber
        if 5.0 < p[0] < 8.0:
            if p[2] == 0 and np.random.rand() < 0.05:
                continue # PM terjerat oleh cairan dan masuk limbah
            if p[2] == 1 and np.random.rand() < 0.025:
                continue # Sebagian CO2 larut oleh NaOH & Dolomit

        # Proses Fiksasi Karbon di Biofilter Mikroalga
        if 10.5 < p[0] < 13.5:
            if p[2] == 1 and np.random.rand() < 0.04:
                p[2] = 2 # CO2 diserap Chlorella vulgaris dan berubah jadi O2

        # Simpan partikel yang belum mencapai batas layar (X = 16.0)
        if p[0] < 16.0:
            surviving_particles.append(p)

    particles = surviving_particles

    # Update jatuhnya air Scrubber
    for w in water_drops: w[1] -= 0.25
    water_drops = [w for w in water_drops if w[1] > 1.0]
    
    # Update naiknya gelembung Biofilter
    for b in bubbles: b[1] += 0.2
    bubbles = [b for b in bubbles if b[1] < 4.5]

    # Render Visualisasi Partikel
    scatter_pm.set_offsets([p[:2] for p in particles if p[2] == 0] or np.empty((0, 2)))
    scatter_co2.set_offsets([p[:2] for p in particles if p[2] == 1] or np.empty((0, 2)))
    scatter_o2.set_offsets([p[:2] for p in particles if p[2] == 2] or np.empty((0, 2)))
    scatter_water.set_offsets(water_drops or np.empty((0, 2)))
    scatter_bubbles.set_offsets(bubbles or np.empty((0, 2)))

    return scatter_pm, scatter_co2, scatter_o2, scatter_water, scatter_bubbles

# Eksekusi Animasi 
ani = animation.FuncAnimation(fig, update, frames=500, interval=40, blit=False)
plt.tight_layout()
ani.save('animasi_orbis.gif', writer='pillow', fps=20)
print("SUKSES! File animasi_orbis.gif sedang dibuat, tunggu sebentar...")
plt.show()