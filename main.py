from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import matplotlib.pyplot as plt
import pandas as pd

# set Chrome options to run in headless mode
def get_driver():
    options = Options()

    return webdriver.Chrome(options=options)

URL_software_eng_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=software engineer&locT=C&locName=New York"
URL_data_sci_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=data scientist&locT=C&locName=New York"
URL_ai_glassdoor = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=machine learning&locT=C&locName=New York"
URL_data_sci_us_gov = "https://www.usajobs.gov/Search/Results?l=New%20York&k=data%20science&p=1"
URL_soft_eng_us_gov = "https://www.usajobs.gov/Search/Results?l=New%20York&p=1&k=software%20engineer"

data_sci = []
software_eng = []
ai = []

# for glassdor
def glassdoor(driver, data):
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

data_col = ['salary','company','location']
df_data_sci = pd.DataFrame(data_sci, columns=data_col)
df_ai = pd.DataFrame(ai, columns=data_col)
df_software = pd.DataFrame(software_eng, columns=data_col)

print('software eng jobs samples: ', len(df_software))
print('data science jobs samples: ', len(df_data_sci))
print('AI jobs samples', len(df_ai))

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
