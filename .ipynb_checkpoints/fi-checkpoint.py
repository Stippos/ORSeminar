#Calculates the financial impact to the bank from payment history row of credit card dataset 
#namely the columns from the 7th column to 26th column or indexes [6:25]

import numpy as np

def impact(paymentHistory):
    
    yearlyFee = 75
    spreadMargin = 0.0125
    collectEff = 0.3
    cashAdvanceFee = 0.05
    avgInterchangeRate = 0.02
    rewardRate = 0.05
    
    #number months when the cutomer is late in their payment times late payment fee
    latePayments = len(np.where(paymentHistory[0:5] > 0)[0])* 20    
    
    #monthly compounging of spread margin on outstanding balance
    interest = 0
    for i in range(6, 12):
        if(paymentHistory[i] > 0):
            interest += paymentHistory[i] * spreadMargin
    
    #calculating money lost on default
    default = 0
    if(paymentHistory[6] > 0):
        default = paymentHistory[6] * paymentHistory[18] * (1 - collectEff)
    
    #taking the outstanding balance on the last month and adding everything that has been paid off
    #to get the total purchase volume of the credit card
    purchaseVolume = paymentHistory[6]
    for i in range(12, 18):
        if(paymentHistory[i] > 0):
            purchaseVolume += paymentHistory[i]
    
    #calculating the purchase volume derivative figures
    interchange = purchaseVolume * avgInterchangeRate    
    rewards = purchaseVolume * rewardRate
    
    #calculating the total outstanding balance from all months
    outstanding = 0
    for i in range(6, 12):
        if(paymentHistory[i] > 0):
            outstanding += paymentHistory[i]
    
    #operating expense of the outstanding balance
    #assumes that customer has on average certain amount of outstanding balance and the opex rate is componded yearly
    opex = outstanding / 6 * 0.05
    
    #estimated purely from the given key values and assumes that everybody is an average customer
    cashAdvance = cashAdvanceFee * 300
    
    #adding up the cashflows
    impact = yearlyFee + latePayments + interest + interchange + cashAdvance - default - opex - rewards
    
    #the financial impact that tries to take into the account the positive bias in the amount of defaulters in the dataset 

    return impact
    
