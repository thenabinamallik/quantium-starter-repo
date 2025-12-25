import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from dash_app import app


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def test_header_present(dash_duo):
    dash_duo.driver = get_driver()
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel Sales Visualiser" in header.text


def test_visualisation_present(dash_duo):
    dash_duo.driver = get_driver()
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None


def test_region_picker_present(dash_duo):
    dash_duo.driver = get_driver()
    dash_duo.start_server(app)

    radio = dash_duo.find_element("#region-filter")
    assert radio is not None
