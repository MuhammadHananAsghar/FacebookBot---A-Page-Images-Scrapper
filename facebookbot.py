from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from tkinter import filedialog
import urllib.request
import datetime
import config

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD


class FacebookBot:
	
	def __init__(self, page):
		"""
		Initializing Bot
		"""
		self.driver_path = "/home/zerosec/Pictures/geckodriver"
		self.path = "https://web.facebook.com/"
		self.page_id = page
		self.bot = webdriver.Firefox(options=self.__options(), executable_path=self.driver_path)
		self.__start(self.bot, self.path)


	def __start(self, bot, path):
		"""
		Starting Bot
		"""
		try:
			bot.get(path)
			WebDriverWait(bot, 8).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
			print("Facebook Loaded")
			if self.__login(bot):
				print("Login Successful")
				self.__scrape(bot, self.page_id)
			else:
				print("Login Failed")
		except:
			print("Failed")


	def __scrape(self, bot, page):
		"""
		Scrapping Faceboot
		"""
		sleep(4)
		bot.get(page)
		print("Page Loading...")
		sleep(10)
		self.__scroll(bot)
		print("Loaded Page")
		path_storage = filedialog.askdirectory()
		data = bot.find_elements_by_tag_name("img")
		img_id = 0
		id = 0
		for image in data:
			img_id += 1
			if img_id > 11:
				self.__save(image.get_attribute("src"), path_storage, id)
				id += 1
			else:
				pass


	def __save(self, image, path, id):
		"""
		Saving Images
		"""
		suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
		filename = "_".join(['page_images', suffix])
		urllib.request.urlretrieve(f"{image}", f"{path}/{str(filename)}_{str(id)}.jpg")
		print("Saved File", str(filename)+".jpg")
		print("Bot Has Saved the Data")
		return


	def __scroll(self, bot):
		"""
		Scrolling the page
		"""
		print("Bot is Scrolling")
		times = 0
		SCROLL_PAUSE_TIME = 2
		# Get scroll height
		last_height = bot.execute_script("return document.body.scrollHeight")
		while True:
		    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		    sleep(SCROLL_PAUSE_TIME)
		    new_height = bot.execute_script("return document.body.scrollHeight")
		    if new_height == last_height:
		        break
		    last_height = new_height
		    times += 1
		    print(f"Scrolled {times} times")
		    if times == 10:
		    	break
		return


	def __login(self, bot):
		"""
		Loging In the Bot
		"""
		try:
			username = bot.find_element_by_xpath('//*[@id="email"]')
			password = bot.find_element_by_xpath('//*[@id="pass"]')
			WebDriverWait(bot, 3)
			username.send_keys(USERNAME)
			WebDriverWait(bot, 3)
			password.send_keys(PASSWORD)
			WebDriverWait(bot, 3)
			bot.find_element_by_xpath('//*[@id="u_0_b"]').click()
			return True
		except:
			return False


	def __options(self):
		"""
		Configuring options of the Bot
		"""
		options = Options()
		options.add_argument("Cache-Control=no-cache")
		options.add_argument("--no-sandbox")
		options.add_argument("--dns-prefetch-disable")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-web-security")
		options.add_argument("--ignore-certificate-errors")
		options.page_load_strategy = 'none'
		options.add_argument("--ignore-certificate-errors-spki-list")
		options.add_argument("--ignore-ssl-errors")
		return options


page = "https://web.facebook.com/BrainyQuote/photos"
fb = FacebookBot(page)