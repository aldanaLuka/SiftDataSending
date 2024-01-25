
code = "CVV_ERROR"

decline_category = {
    
    "additional_verification_required": [
        "THREE_D_SECURITY_AUTHENTICATION_REQUIRED", 
        "STRONG_CUSTOMER_AUTHENTICATION_REQUIRED"
    ],
    
    "bank_decline": [
        "INVALID_TRANSACTION",
        "TRANSACTION_NOT_AUTHORIZED"
    ],

    "expired": [
        "EXPIRED_CARD"
    ],

    "fraud": [
        "FRAUD_DETECTED",
        "FRAUD_ERROR"
    ],

    "insufficient_funds": [
        "INSUFFICIENT_FUNDS"
    ],

    "invalid": [
        "MISSING_SHOPPER_OR_CARD_HOLDER",
        "MISSING_CARD_TYPE",
        "INVALID_API_VERSION",
        "INVALID_MERCHANT_TRANSACTION_ID",
        "INVALID_RECURRING_TRANSACTION",
        "MERCHANT_CONFIGURATION_ERROR",
        "MISSING_CARD_TYPE",
        "INCORRECT_SETUP",
        "INVALID_AMOUNT",
        "PROCESSING_AMOUNT_ERROR",
        "PAYMENT_METHOD_NOT_SUPPORTED",
        "SHOPPER_NOT_FOUND",
        "MULTIPLE_PAYMENT_METHODS_NON_SELECTED",
        "TRANSACTION_ALREADY_EXISTS",
        "TRANSACTION_EXPIRED",
        "TRANSACTION_ID_REQUIRED",
        "INVALID_TRANSACTION_ID",
        "TRANSACTION_CARD_NOT_VALID",
        "MISSING_RELEVANT_METHOD_FOR_SHOPPER",
        "EXTERNAL_TAX_SERVICE_MISMATCH_CURRENCY",
        "EXTERNAL_TAX_SERVICE_UNEXPECTED_TOTAL_PAYMENT",
        "EXTERNAL_TAX_SERVICE_TAX_REFERENCE_ALREADY_USED"
    ],

    "invalid_verification": [
        "VALIDATION_GENERAL_FAILURE",
        "AUTHORIZATION_AMOUNT_ALREADY_REVERSED",
        "AUTHORIZATION_AMOUNT_NOT_VALID",
        "AUTHORIZATION_EXPIRED",
        "AUTHORIZATION_REVOKED",
        "AUTHORIZATION_NOT_FOUND",
        "CVV_ERROR",
        "INCORRECT_INFORMATION",
        "INVALID_CARD_NUMBER",
        "INVALID_CARD_TYPE",
        "INVALID_PIN_OR_PW_OR_ID_ERROR",
        "THREE_D_SECURE_FAILURE",
        "CREDIT_CARD_DETAILS_PLAIN_AND_ENCRYPTED",
        "CREDIT_CARD_ENCRYPTED_NUMBER_REQUIRED",
        "CREDIT_CARD_ENCRYPTED_SECURITY_CODE_REQUIRED",
        "USER_NOT_AUTHORIZED"
    ],

    "limit_exceeded": [
        "LIMIT_EXCEEDED"
    ],

    "lost_or_stolen": [
        "CARD_LOST_OR_STOLEN",
        "PICKUP_CARD"
    ],

    "other": [
        "INVALID_TRANSACTION_TYPE",
        "INVALID_HTTP_METHOD",
        "PAYMENT_GENERAL_FAILURE",
        "BLS_CONNECTION_PROBLEM",
        "CALL_ISSUER",
        "GENERAL_PAYMENT_PROCESSING_ERROR",
        "PROCESSING_DUPLICATE",
        "PROCESSING_GENERAL_DECLINE",
        "PROCESSING_TIMEOUT",
        "REFUND_FAILED",
        "RESTRICTED_CARD",
        "SYSTEM_TECHNICAL_ERROR",
        "THE_ISSUER_IS_UNAVAILABLE_OR_OFFLINE",
        "NO_AVAILABLE_PROCESSORS",
        "MULTIPLE_TRANSACTIONS_FOUND",
        "TRANSACTION_LOCKED",
        "TRANSACTION_PAYMENT_METHOD_NOT_SUPPORTED",
        "TRANSACTION_ALREADY_CAPTURED",
    ],

    "risky": [
        "XSS_EXCEPTION",
        "ACCOUNT_CLOSED",
        "DO_NOT_HONOR",
        "HIGH_RISK_ERROR",
        "SHOPPER_COUNTRY_OFAC_SANCTIONED"
    ],


    
}

for sift_category, bluesnap_categories in decline_category.items():
    if code in bluesnap_categories:
        final_sift_category = sift_category
        break 
    
print(final_sift_category)