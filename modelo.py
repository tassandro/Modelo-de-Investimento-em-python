import yfinance as yf
import pandas as pd
!pip install QuantStats
import quantstats as qs

composicao_historica = pd.read_excel(r'C:\Users\Tassandro\Downloads\composicao_ibov (2).xlsx')

lista_acoes = pd.read_excel(r'C:\Users\Tassandro\Downloads\composicao_ibov (2).xlsx', sheet_name = 'lista_acoes')

dados_cotacoes = (yf.download(lista_acoes['tickers'].to_list(), 
                              start = "2015-06-30", end = "2022-12-31")['Adj Close'])

dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)

dados_cotacoes = dados_cotacoes.sort_index()

r6 = (dados_cotacoes.resample("M").last().pct_change(periods = 6).
                        dropna(axis = 0, how = "all").drop("2022-12-31"))

for data in r6.index:
    for empresa in r6.columns:
        
        if empresa.replace(".SA", "") not in composicao_historica.loc[:, data].to_list():
        
            r6.loc[data, empresa] = pd.NA
          
carteiras = r6.rank(axis = 1, ascending = False).applymap(lambda x: 1 if x < 11 else 0)

retorno_mensal = dados_cotacoes.resample("M").last().pct_change(periods = 1)

retorno_mensal = retorno_mensal.drop(retorno_mensal.index[:7], axis = 0)

carteiras.index = retorno_mensal.index

retorno_modelo = (retorno_mensal * carteiras).sum(axis = 1)/10

qs.extend_pandas()

retorno_modelo.plot_monthly_heatmap()

ibovespa = yf.download("^BVSP", start = "2015-12-30", end = "2022-12-31")['Adj Close']

ibovespa = ibovespa.resample("M").last().pct_change().dropna()

retorno_acum_modelo = (1 + retorno_modelo).cumprod() - 1 
retorno_acum_ibov =  (1 + ibovespa).cumprod() - 1

retorno_acum_modelo.plot_monthly_heatmap()
retorno_acum_ibov.plot_monthly_heatmap()

ganhos_modelo = retorno_modelo - ibovespa

ganhos_modelo.plot_monthly_heatmap()



