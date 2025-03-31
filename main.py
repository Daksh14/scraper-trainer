
import matplotlib.pyplot as plt
import pandas as pdfrom
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import time

import matplotlib.pyplot as plt
import pandas as pd
from token import OP

# set Chrome options to run in headless mode
def get_driver():
    options = Options()

    return webdriver.Chrome(options=options)

URL_software_eng_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=software engineer&locT=C&locName=New York"
URL_data_sci_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=data scientist&locT=C&locName=New York"
URL_ai_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=machine learning&locT=C&locName=New York"
URL_data_sci_us_gov = "https://www.usajobs.gov/Search/Results?l=New%20York&k=data%20science&p=1"
URL_soft_eng_us_gov = "https://www.usajobs.gov/Search/Results?l=New%20York&p=1&k=software%20engineer"
URL_software_eng_sh = "https://www.simplyhired.com/search?q=software+engineer&l="
URL_data_sci_sh = "https://www.simplyhired.com/search?q=data+science&l="
URL_ai_sh = "https://www.simplyhired.com/search?q=artifical+intellgence&l="

data_sci = []
software_eng = []
ai = []

def click_load_more(driver):
    try:
        load_more_button = "button[data-test='load-more']"
        button = driver.find_element(By.CSS_SELECTOR, load_more_button)

        if button is not None:
            button.click()
    except:
       pass

# for glassdor
def glassdoor(driver, data):
    for _ in range(10):
        click_load_more(driver)
        time.sleep(2)

    elements = driver.find_elements(By.CSS_SELECTOR, "li.JobsList_jobListItem__wjTHv")

    for e in elements:
        try:
            salary = e.find_element(By.CSS_SELECTOR, ".JobCard_salaryEstimate__QpbTW").text
            loc = e.find_element(By.CSS_SELECTOR, ".JobCard_location__Ds1fM").text
            comp = e.find_element(By.CSS_SELECTOR, ".EmployerProfile_compactEmployerName__9MGcV").text
            salary = salary.replace("(Employer est.)", "").replace("$", "")
            salary = salary[0:4]
            salary = salary.replace('K', '')

            salary = int(salary) * 1000
            data.append([salary, comp, loc])
        except:
            print('e glassdor')

def us_gov(driver, data):
    elements = driver.find_elements(By.CSS_SELECTOR, ".usajobs-search-result--core")
    company = "US Government"

    for e in elements:
        try:
            salary = e.find_element(By.CSS_SELECTOR, ".usajobs-search-result--core__item").text
            salary = salary.replace("Starting at ", "")
            salary = salary[0:8]
            salary_int = int(salary.replace("$", "").replace(",", ""))
            location = e.find_element(By.CSS_SELECTOR, ".usajobs-search-result--core__location-link").text
            data.append([salary_int, company, location])
        except:
            print('err us gov')

def words_before_target(text, target):
    words = text.split()
    
    if target in words:
        index = words.index(target)
        return " ".join(words[:index])
    else:
        return None



def click_next_page(driver, button_num):
    try:
        n = str(button_num)
        load_more_button = "a[aria-label='page ${n}']"
        button = driver.find_element(By.CSS_SELECTOR, load_more_button)

        if button is not None:
            button.click()
    except:
       pass

def simplyhired(driver, data):
    elements = driver.find_elements(By.CSS_SELECTOR, ".css-obg9ou")

    for e in elements:
        try:
            salary = 0
            try:
                salary = e.find_element(By.CSS_SELECTOR, "p[data-testid='searchSerpJobSalaryConfirmed']").text
            except NoSuchElementException:
                salary = e.find_element(By.CSS_SELECTOR, "p[data-testid='searchSerpJobSalaryEst']").text

            location = e.find_element(By.CSS_SELECTOR, "span[data-testid='searchSerpJobLocation']").text
            company = e.find_element(By.CSS_SELECTOR, "span[data-testid='companyName']").text
            
            salary_int = 0

            if "an hour" in salary:
                salary = salary.replace("From ", "")
                salary = salary.replace("an hour", "")
                if "-" in salary:
                     salary = words_before_target(salary, "-")
                     
                salary = salary.replace("$", "")
                
                # approx 2,080 working hours in an year
                salary_int = int(salary) * 2080
            elif "Estimated" in salary:
                salary = salary.replace("Estimated:", "")
                salary = salary.replace("a year", "")
                
                
                salary_a = words_before_target(salary, "K")

                if salary_a is None:
                    salary = words_before_target(salary, "-")
                else:
                    salary = salary_a

                salary = salary.replace("$", "")
                salary = salary.replace(".", "")
                salary = salary.replace("K", "")

                try:
                    salary_int = int(salary)
                except ValueError:
                    salary_int = int(float(salary))

                salary_int = salary_int * 1000
            else:
                salary = salary.replace("a year", "")
                salary_a = words_before_target(salary, "K")
                if salary_a is None:
                    salary = words_before_target(salary, "-")
                else:
                    salary = salary_a
                salary = salary.replace("$", "")
                salary = salary.replace(",", "")
                                
                try:
                    salary_int = int(salary)
                except ValueError:
                    salary_int = int(float(salary))

            data.append([salary_int, company, location])
        except:
            print("simply hired")

# for us gov jobs
driver = get_driver()
driver.get(URL_data_sci_us_gov)
us_gov(driver, data_sci)
driver.quit()

driver = get_driver()
driver.get(URL_soft_eng_us_gov)
us_gov(driver, software_eng)
driver.quit()

# for glassdor
driver = get_driver()
driver.get(URL_data_sci_glassdoor)
glassdoor(driver, data_sci)
driver.quit()

driver = get_driver()
driver.get(URL_software_eng_glassdoor)
glassdoor(driver, software_eng)
driver.quit()

driver = get_driver()
driver.get(URL_ai_glassdoor)
glassdoor(driver, ai)
driver.quit()

pages_sh = 5

driver = get_driver()
driver.get(URL_software_eng_sh)

for i in range(0, 30):
    simplyhired(driver, software_eng)
    click_next_page(driver, i)

driver.quit()

print(software_eng)

driver = get_driver()
driver.get(URL_data_sci_sh)

for i in range(0, pages_sh):    
    simplyhired(driver, data_sci)
    click_next_page(driver, i)

driver.quit()

driver = get_driver()
driver.get(URL_ai_sh)

for i in range(0, pages_sh):
    simplyhired(driver, ai)
    click_next_page(driver, i)

driver.quit()

data_col = ['salary','company','location']
df_data_sci = pd.DataFrame(data_sci, columns=data_col)
df_ai = pd.DataFrame(ai, columns=data_col)
df_software = pd.DataFrame(software_eng, columns=data_col)

full = pd.concat([df_data_sci, df_ai, df_software], axis=0)

full.to_csv('jobs.csv', index=False)

def train_linear_regression(X, y, title):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print('mse: ', mse)
    # plot the results
    plt.scatter(y_test, y_pred)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.title('Linear regression ' + title)
    plt.show()

# train logisiic regression
def train_logistic_regression(X, y, title):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print('mse: ', mse)
    # plot the results
    plt.scatter(y_test, y_pred)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.title('Logistic regression ' + title)
    plt.show()



print(df_software)
print(df_data_sci)
print(df_ai)
# for software enginner use linear regression model to predict salary

X = df_software.drop('salary', axis=1)
y = df_software['salary']

# use lable encoder to encode the company and location
le = LabelEncoder()
X['company'] = le.fit_transform(X['company'])
X['location'] = le.fit_transform(X['location'])

train_linear_regression(X, y, 'Software Engineer Salary Prediction')
train_logistic_regression(X, y, 'Software Engineer Salary Prediction')

# for data scientist use linear regression model to predict
X = df_data_sci.drop('salary', axis=1)
y = df_data_sci['salary']

# use lable encoder to encode the company and location
le = LabelEncoder()
X['company'] = le.fit_transform(X['company'])
X['location'] = le.fit_transform(X['location'])

train_linear_regression(X, y, 'Data Scientist Salary Prediction')
train_logistic_regression(X, y, 'Data Scientist Salary Prediction')

# for AI use linear regression model to predict
X = df_ai.drop('salary', axis=1)
y = df_ai['salary']

# use lable encoder to encode the company and location
le = LabelEncoder()
X['company'] = le.fit_transform(X['company'])
X['location'] = le.fit_transform(X['location'])

train_linear_regression(X, y, 'AI Salary Prediction')
train_logistic_regression(X, y, 'AI Salary Prediction')
