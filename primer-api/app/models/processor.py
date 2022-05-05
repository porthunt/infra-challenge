from enum import Enum


class Processor(Enum):
    BRAINTREE = "BRAINTREE"
    ADYEN = "ADYEN"
    STRIPE = "STRIPE"
    PAYPAL = "PAYPAL"
    GOCARDLESS = "GOCARDLESS"
    INGENICO = "INGENICO"
