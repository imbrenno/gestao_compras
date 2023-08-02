from enum import Enum


class SuplierPaymentTypesEnum(Enum):
    PIX = "pix"
    BILL_PAYMENT = "bill_payment"
    TED = "ted"
    CARD = "card"
    def __str__(self):
        return self.value