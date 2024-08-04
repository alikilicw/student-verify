# Temel imaj olarak resmi Python imajını kullanıyoruz
FROM python:3.12.4

# Gerekli paketleri yükle
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    unzip

# Geckodriver'ı indir ve kur
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.33.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.33.0-linux64.tar.gz

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Gereksinimler dosyasını çalışma dizinine kopyala
COPY requirements.txt .

# Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını çalışma dizinine kopyala
COPY . .

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
