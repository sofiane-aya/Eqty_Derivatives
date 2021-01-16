import numpy as np
import random as rd
import scipy.stats as sp


#region Black Scholes ergfz

def d1(S,K,T,R,sigma):return ((np.log(S/K)+(R+0.5 * pow(sigma,2))*T)/(sigma * pow(T,0.5)))

def d2(S,K,T,R,sigma):return d1(S,K,T,R,sigma) - sigma * pow(T,0.5)

def Call_Price_BS(S,K,T,R,sigma):return S * sp.norm.cdf(d1(S,K,T,R,sigma),0,1) - K * np.exp(-R * T) * sp.norm.cdf(d2(S,K,T,R,sigma),0,1)

def Put_Price_BS(S,K,T,R,sigma):return -S * sp.norm.cdf(-d1(S,K,T,R,sigma),0,1) + K * np.exp(-R * T) * sp.norm.cdf(-d2(S,K,T,R,sigma),0,1)

def Delta(S,K,T,R,sigma, isCall = True):

    if isCall == True:

        return sp.norm.cdf(d1(S,K,T,R,sigma),0,1)

    else:

        return sp.norm.cdf(d1(S,K,T,R,sigma),0,1) - 1

def Gamma(S,K,T,R,sigma):return sp.norm.pdf(d1(S,K,T,R,sigma))/ (S * sigma * pow(T,0.5))

def Vega(S,K,T,R,sigma):return S * sp.norm.pdf(d1(S,K,T,R,sigma))* pow(T,0.5)

def Tetha(S,K,T,R,sigma, isCall = True):

    if isCall == True:

        return (-S * sp.norm.pdf(d1(S,K,T,R,sigma)) * sigma / (2*pow(T,0.5))) - R * K * np.exp(-R*T) * sp.norm.cdf(d2(S,K,T,R,sigma),0,1)

    else:

        return (-S * sp.norm.pdf(d1(S,K,T,R,sigma)) * sigma / (2*pow(T,0.5))) + R * K * np.exp(-R*T) * sp.norm.cdf(-d2(S,K,T,R,sigma),0,1)

def Rho(S,K,T,R,sigma, isCall = True):

    if isCall == True :

        return K * T * np.exp(-R*T) * sp.norm.cdf(d2(S,K,T,R,sigma))

    else:

        return -K * T * np.exp(-R*T) * sp.norm.cdf(-d2(S,K,T,R,sigma))

def implied_Volatility(S,K,T,R,Price,Sigma0, Epsilon, isCall = True):

    x = Sigma0

    if isCall == True:
        while Price - Call_Price_BS(S,K,T,R,x)/Vega(S,K,T,R,x) > Epsilon:

            dx = Vega(S,K,T,R,x)
            x = x - Price - Call_Price_BS(S,K,T,R,x)/dx
    else:
        while Price - Put_Price_BS(S, K, T, R, x) / Vega(S, K, T, R, x) > Epsilon:
            dx = Vega(S, K, T, R, x)
            x = x - Price - Put_Price_BS(S, K, T, R, x) / dx

    return x
