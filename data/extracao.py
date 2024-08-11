from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime ##EXCLUIR
import pandas as pd

# Captura a data atual
data_atual = datetime.now()

# Formata a data no formato desejado 'AAAA-MM-DD'
data_formatada = data_atual.strftime('%Y%m%d')

# Nome do arquivo CSV
csv_filename = f'dados_imoveis_{data_formatada}.csv'

# Configurações do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--log-level=OFF")

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessa a página desejada
url = "https://www.zapimoveis.com.br/venda/imoveis/ce+fortaleza"
driver.get(url)

time.sleep(30)

# Abre o arquivo CSV para escrita
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escreve o cabeçalho no CSV
    writer.writerow(['Link', 'Metragem', 'Quartos', 'Banheiros', 'Vagas', 'Animais'
                     , 'Piscina', 'Varanda', 'Elevador', 'Ar-condicionado', 'Churrasqueira'
                     , 'Cozinha', 'Quadra', 'Área de Serviço', 'Preço', 'Condomínio', 'IPTU'])
    # Rola a página lentamente até que o elemento de passar página esteja visível
    while True:
        try:
            # Tenta encontrar o elemento de paginação
            # elemento_alvo = WebDriverWait(driver, timeout=.2).until(
            #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/section/div/form/div[2]/div[4]/div[1]/div/section/nav'))
            # )

            # Após encontrar a paginação, inicia o processo de extração dos dados
            # Puxando apenas os imoveis que estão disponíveis no site

            divs = driver.find_elements(By.CSS_SELECTOR, "div.BaseCard_card__Ci4Ny")

            # Itera sobre cada elemento
            for div in divs:
                try:
                    #Tenta acessar a página do imovel em uma nova aba
                    imovel = div.find_element(By.CSS_SELECTOR, 'BaseCard_card__Ci4Ny')
                    # actions = ActionChains(driver)
                    # actions.key_down(Keys.CONTROL).click(imovel).key_up(Keys.CONTROL).perform()
                    div.execute_script("window.open(arguments[0].href);", imovel) 
                    print('----------------------------------------------------ENTROU AQUI?----------------------------------------------------')

                    time.sleep(3)

                    # Alterna para a nova aba aberta
                    driver.switch_to.window(driver.window_handles[-1])

                    try:
                        # Localiza o bloco que contém os dados do imóvel
                        amenities_block = driver.find_element(By.XPATH, "//div[@class='amenities-list']")

                        metragem = amenities_block.find_element(By.XPATH, ".//p[@itemprop='floorSize']//span[@class='amenities-item-text']").text
                        quartos = amenities_block.find_element(By.XPATH, ".//p[@itemprop='numberOfRooms']//span[@class='amenities-item-text']").text
                        banheiros = amenities_block.find_element(By.XPATH, ".//p[@itemprop='numberOfBathroomsTotal']//span[@class='amenities-item-text']").text
                        vagas = amenities_block.find_element(By.XPATH, ".//p[@itemprop='numberOfParkingSpaces']//span[@class='amenities-item-text']").text
                        animais = amenities_block.find_element(By.XPATH, ".//p[@itemprop='PETS_ALLOWED']//span[@class='amenities-item-text']").text
                        piscina = amenities_block.find_element(By.XPATH, ".//p[@itemprop='POOL']//span[@class='amenities-item-text']").text
                        varanda = amenities_block.find_element(By.XPATH, ".//p[@itemprop='BALCONY']//span[@class='amenities-item-text']").text
                        elevador = amenities_block.find_element(By.XPATH, ".//p[@itemprop='ELEVATOR']//span[@class='amenities-item-text']").text
                        ar_condicionado = amenities_block.find_element(By.XPATH, ".//p[@itemprop='AIR_CONDITIONING']//span[@class='amenities-item-text']").text
                        churrasqueira = amenities_block.find_element(By.XPATH, ".//p[@itemprop='BARBECUE_GRILL']//span[@class='amenities-item-text']").text
                        cozinha = amenities_block.find_element(By.XPATH, ".//p[@itemprop='KITCHEN']//span[@class='amenities-item-text']").text
                        quadra = amenities_block.find_element(By.XPATH, ".//p[@itemprop='SPORTS_COURT']//span[@class='amenities-item-text']").text
                        area_servico = amenities_block.find_element(By.XPATH, ".//p[@itemprop='SERVICE_AREA']//span[@class='amenities-item-text']").text

                        # Extrai o link do imovel
                        link_element = driver.find_element(By.XPATH, "//link[@rel='canonical']")
                        link = link_element.get_attribute('href')

                        # Localiza o bloco que contém as informações de preço
                        price_info_block = driver.find_element(By.CLASS_NAME, "price-info-wrapper")

                        preco = price_info_block.find_element(By.XPATH, ".//p[@data-testid='price-info-value']").text
                        condominio = price_info_block.find_element(By.XPATH, ".//span[@id='condo-fee-price']").text
                        iptu = price_info_block.find_element(By.XPATH, ".//span[@id='iptu-price']").text

                        # Imprime as informações extraídas
                        print(link,metragem, quartos, banheiros, vagas, animais, piscina,
                                         varanda, elevador, ar_condicionado, churrasqueira, 
                                         cozinha, quadra, area_servico, preco, condominio, iptu)

                        # Escreve as informações extraídas no arquivo CSV
                        writer.writerow([link,metragem, quartos, banheiros, vagas, animais, piscina,
                                         varanda, elevador, ar_condicionado, churrasqueira, 
                                         cozinha, quadra, area_servico, preco, condominio, iptu])

                        # Fecha a aba atual
                        driver.close()
                        
                        # Clica no botão de passar para a próxima página
                        # elemento_alvo.click()

                        #Reinicia o for
                        pass

                    except:
                        # Fecha a aba atual
                        # driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        pass
                
                except:
                    # Fecha a aba atual
                    # driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            
        except:
            # Se o elemento não for encontrado ou não estiver visível, rola a página para baixo em pequenos incrementos
            driver.execute_script("window.scrollBy(0, 300);")
    
            # Verifica se chegou ao final da página (se necessário)
            if driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight"):
                print("Elemento não encontrado na página.")
                break

# Fechar o navegador
driver.quit()