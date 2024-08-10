from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time as t
import string
import pandas as pd

# Configurações do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--log-level=OFF")

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessa a página desejada
url = "https://www.zapimoveis.com.br/venda/imoveis/ce+fortaleza/?__ab=sup-hl-pl:newC,exp-aa-test:control,super-high:new,olx:control,phone-page:new,off-no-hl:new&transacao=venda&onde=,Cear%C3%A1,Fortaleza,,,,,city,BR%3ECeara%3ENULL%3EFortaleza,-3.906286,-38.387474,&pagina=1"
driver.get(url)

# Espera o carregamento da página (opcional, dependendo da complexidade da página)
driver.implicitly_wait(10)

# Encontrar todos os elementos div com o seletor adequado
# listing_wrapper_content = driver.find_element(By.CLASS_NAME, 'listing-wrapper__content')

# Encontra todos os elementos div dentro do contêiner
# divs = listing_wrapper_content.find_elements(By.TAG_NAME, 'div')

divs = driver.find_elements(By.CSS_SELECTOR, "div.BaseCard_card__Ci4Ny")

# Itera sobre cada div e seus filhos
for div in divs:
    try:
        # Extrai o preço
        preco_element = div.find_element(By.XPATH, ".//p[contains(@class, 'l-text') and contains(text(), 'R$')]")
        preco = preco_element.text if preco_element else 'N/A'

        # Extrai a metragem (ex: "60 m²")
        metragem_element = div.find_element(By.XPATH, ".//p[contains(@data-cy, 'rp-cardProperty-propertyArea-txt')]")
        metragem = metragem_element.text if metragem_element else 'N/A'

        # Extrai o número de quartos
        quartos_element = div.find_element(By.XPATH, ".//p[contains(@data-cy, 'rp-cardProperty-bedroomQuantity-txt')]")
        num_quartos = quartos_element.text if quartos_element else 'N/A'

        # Extrai o número de banheiros
        banheiros_element = div.find_element(By.XPATH, ".//p[contains(@data-cy, 'rp-cardProperty-bathroomQuantity-txt')]")
        num_banheiros = banheiros_element.text if banheiros_element else 'N/A'

        # Extrai o bairro e a cidade
        localizacao_element = div.find_element(By.XPATH, ".//h2[contains(@data-cy, 'rp-cardProperty-location-txt')]")
        localizacao = localizacao_element.text if localizacao_element else 'N/A'

        # Imprime as informações extraídas
        print(f"Bairro e Cidade: {localizacao}")
        print(f"Metragem: {metragem}")
        print(f"Quartos: {num_quartos}")
        print(f"Banheiros: {num_banheiros}")
        print(f"Preço: {preco}")
        print("-----")
        
    except Exception as e:
        print(f"Erro ao extrair informações")

# Fechar o navegador
driver.quit()