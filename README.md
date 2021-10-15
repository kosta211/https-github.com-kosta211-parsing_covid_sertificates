# Parsing COVID-sertificates
Usage example:

```
>  python main.py [certificate_covid.pdf] [output.json]
```
  
Output example:

```javascript
{
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Иванович",
    "birthday": "01-01-1970",
    "sex": "Мужской",
    "document": "3215 №430543",
    "vaccine": {
        "date": "03.07.2021",
        "preparation": "Гам-КОВИД-Вак Комбинированная векторная вакцина для профилактикикоронавирусной инфекции, вызываемой вирусом SARS-CoV-2"
    }
}
```