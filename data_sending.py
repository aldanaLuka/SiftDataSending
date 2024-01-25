import psycopg2
import json
import requests
#import sift

#client = sift.Client(api_key='{6a60d865d2af9bde}', account_id='{6581f47eae2429766a707d53}')  

def send(api_url = "https://api.sift.com/v205/events", data={}):
    response = requests.post(api_url, json=data)
    response.json()
    print(response)
    

def json_creation_transaction(rows):

    for TX in rows: 
        
        if TX[7] =="Tx Exitosa":    
            properties = {

                "$type" : "$transaction", 
                "$api_key" : "6a60d865d2af9bde", 
                "$user_id"          : TX[5].lower(),
                "$amount"           : int(float(TX[4])*1000000), 
                "$currency_code"    : TX[3],

                "$user_email"                : TX[5].lower(),
                "$order_id"                  : str(TX[0]),
                "$transaction_id"            : str(TX[0]),
                "$transaction_type"          : get_transaction_type(TX[7]),
                "$transaction_status" : get_status(TX[7]),
                "$ip" : TX[1],
                "$time" : int(TX[2].timestamp()), 

                "$payment_method"   : {
                    "$payment_type"    : "$credit_card",  #11
                    "$payment_gateway" : "$bluesnap", #9
                    "$account_holder_name" : TX[6],
                    "$card_bin"        : get_card_info(TX[10], True),
                    "$card_last4"      : get_card_info(TX[10], False),
                    },
                
                "$merchant_profile" : {
                    "$merchant_id": str(TX[14]),
                    "$merchant_name": TX[8]
                }
            }
            
        else: 
            
            properties = {
                "$type" : "$transaction", 
                "$api_key" : "6a60d865d2af9bde", #***************
                "$user_id"          : TX[5].lower(),
                "$amount"           : int(float(TX[4])*1000000), 
                "$currency_code"    : TX[3],

                "$user_email"                : TX[5].lower(),
                "$decline_category"          : decline_category(TX[13]),
                "$order_id"                  : str(TX[0]),
                "$transaction_id"            : str(TX[0]),
                "$transaction_type"            : get_transaction_type(TX[7]),
                "$transaction_status" : get_status(TX[7]),
                "$ip" : TX[1],
                "$time" : int(TX[2].timestamp()), 

                "$payment_method"   : {
                    "$payment_type"    : "$credit_card", 
                    "$payment_gateway" : "$bluesnap",
                    "$account_holder_name" : TX[6],
                    #"$card_bin"        : get_card_info(TX[10], True),
                    "$card_last4"      : get_card_info(TX[10], False),
                    },
                
                "$merchant_profile" : {
                    "$merchant_id": str(TX[14]),
                    "$merchant_name": TX[8]
                }
            }
        print("")
        print(properties)
        #send(data = properties)
        #response = client.track("$transaction", properties)
        
    
def json_creation_create_order(rows): 
    
    for TX in rows: 
    
        properties = {

            "$type" : "$create_order", 
            "$api_key" : "6a60d865d2af9bde", 
            "$user_id"          : TX[5].lower(),
            "$amount"           : int(float(TX[4])*1000000), 
            "$currency_code"    : TX[3],
    
            "$user_email"                : TX[5].lower(),
            "$order_id"                  : str(TX[0]),
            "$ip" : TX[1],
            "$time" : TX[2].timestamp(), 

            "$payment_method"   : {
                "$payment_type"    : "$credit_card", 
                "$payment_gateway" : "$bluesnap",
                "$account_holder_name" : TX[6],
                #"$card_bin"        : get_card_info(TX[10], True),
                "$card_last4"      : get_card_info(TX[10], False),
                },
            
            "$merchant_profile" : {
                "$merchant_id": str(TX[14]),
                "$merchant_name": TX[8]
            }
        }
        
        print(properties)
        print("")
        #send(data = properties)
        #response = client.track("$create_order", properties)

def get_transaction_type(estatus): 
    match estatus: 
        case "Tx Exitosa":
            return "$sale"
        case "Tx Fallida":
            return "$sale"
        case "Reembolso Exitoso":
            return "$refund"
        case _: 
            return "$sale"

def get_card_info(n, bin): 
    result = ""
    if bin:        
        for x in range(0,6):  
            result += n[x]
    else:
        result += n[-4]
        result += n[-3]
        result += n[-2]
        result += n[-1] 
    return result

def decline_category(respuesta_bluesnap_str):
    
    respuesta_bluesnap = json.loads(respuesta_bluesnap_str)   
    code = respuesta_bluesnap["message"][0]["errorName"]

    decline_category_dict = {
    
    "$additional_verification_required": [
        "THREE_D_SECURITY_AUTHENTICATION_REQUIRED", 
        "STRONG_CUSTOMER_AUTHENTICATION_REQUIRED"
    ],
    
    "$bank_decline": [
        "INVALID_TRANSACTION",
        "TRANSACTION_NOT_AUTHORIZED"
    ],

    "$expired": [
        "EXPIRED_CARD"
    ],

    "$fraud": [
        "FRAUD_DETECTED",
        "FRAUD_ERROR"
    ],

    "$insufficient_funds": [
        "INSUFFICIENT_FUNDS_FOR_REFUND",
        "INSUFFICIENT_FUNDS"
    ],

    "$invalid": [
        "AUTHORIZATION_NEEDED_BEFORE_CAPTURE",
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

    "$invalid_verification": [
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

    "$limit_exceeded": [
        "LIMIT_EXCEEDED"
    ],

    "$lost_or_stolen": [
        "CARD_LOST_OR_STOLEN",
        "PICKUP_CARD"
    ],

    "$other": [
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
        "AMOUNT_EXCEEDED_MAXIMUM_ALLOWED_FRACTION_DIGITS",
        "BLS_ECP_WRONG_BANK_DETAILS",
        "BLS_ERROR_IN_PROCESSING_SUBSCRIPTION_PAYMENT",
        "BLS_NO_SUCH_SHOPPER_PAYMENT_METHOD",
        "CART_OR_CART_PARAMS_REQUIRED",
        "CDOD_NOT_SUPPORTED_IN_CART",
        "CHANGING_SUBSCRIPTION_SKU_NOT_SUPPORTED",
        "CLIENT_ENCRYPTION_BAD_INPUT",
        "CLIENT_ENCRYPTION_BAD_PUBLIC_KEY",
        "CLIENT_ENCRYPTION_GENERAL_FAILURE",
        "COUPON_CODE_REQUIRED",
        "COUPON_NOT_FOUND",
        "ONLY_ONE_COUPON_PER_ORDER",
        "CURRENCY_CODE_NOT_FOUND",
        "CUSTOM_PARAMETER_NOT_FOUND",
        "EDW_NOT_SUPPORTED_IN_CART",
        "EMPTY_CART",
        "EMPTY_RESULT",
        "EXPECTED_TOTAL_PRICE_FAILURE",
        "FAILED_CREATING_PAYPAL_TOKEN",
        "ILLEGAL_PAYPAL_ORDER_STATUS",
        "INACTIVE_SUBSCRIPTION",
        "INVALID_AFFILIATE_ID",
        "INVALID_BANK_COUNTRY",
        "INVALID_CANCELLATION_REASON",
        "INVALID_CURRENCY",
        "INVALID_CUSTOM_PARAMETER",
        "INVALID_INPUT",
        "INVALID_IP_ADDRESS",
        "INVALID_NUM_OF_SHOPPER_PAYMENT_METHODS",
        "INVALID_PAGE_NAME",
        "INVALID_SHOPPER_ID",
        "INVALID_SKU_PARAMETER",
        "INVALID_STEP_FIELD",
        "INVALID_VAT_ID",
        "INVOICE_ALREADY_REFUNDED",
        "INVOICE_ALREADY_FULLY_REFUNDED",
        "INVOICE_ID_NOT_FOUND",
        "LICENSE_KEY_REGENERATION_GENERAL_FAILURE",
        "MISSING_PARAMETER_KEY_OR_VALUE",
        "NEGATIVE_AMOUNT_FAILURE",
        "NEXT_CHARGE_AMOUNT_REQUIRED",
        "NEXT_CHARGE_CURRENCY_REQUIRED",
        "NEXT_CHARGE_NEGATIVE_AMOUNT_FAILURE",
        "NO_SHOPPER_FOR_SUBSCRIPTION_ID",
        "NON_POSITIVE_AMOUNT_FAILURE",
        "NON_POSITIVE_QUANTITY",
        "ORDER_INVOICE_OR_SUBSCRIPTION_ID_REQUIRED",
        "ORDER_NOT_FOUND",
        "PARTIAL_REFUND_AMOUNT_REQUIRED",
        "PARTIAL_REFUND_INVALID_AMOUNT",
        "PARTIAL_REFUND_INVALID_SKU",
        "PARTIAL_REFUND_INVALID_SKU_REFUND_AMOUNT",
        "PARTIAL_REFUND_MORE_THAN_ONE_SKU",
        "PARTIAL_REFUND_NOT_SUPPORTED",
        "PARTIAL_REFUND_SKU_ERROR",
        "PARTIAL_REFUND_SKU_AMOUNT_MAX_AMOUNT_FAILURE",
        "PAYMENT_INFO_REQUIRED",
        "PAYMENT_METHOD_NOT_REFUNDABLE",
        "PAYPAL_CUSTOM_PLAN_NOT_SUPPORTED",
        "PAYPAL_SUBSCRIPTION_DATA_MISMATCH",
        "PAYPAL_TOO_MANY_SUBSCRIPTIONS",
        "PERSISTED_SHOPPING_CONTEXT_NOT_FOUND",
        "PLAN_CHANGE_WITH_MORE_THAN_ONE_SKU",
        "REFUND_GENERAL_FAILURE",
        "REFUND_IN_PROCESS",
        "REFUND_MAX_AMOUNT_FAILURE",
        "REFUND_MIN_AMOUNT_FAILURE",
        "REFUND_ORDER_WITH_ZERO_TOTAL_AMOUNT",
        "REFUND_PERIOD_EXPIRED",
        "REFUND_WITHOUT_REFUNDABLE_PAYMENTS",
        "SELLER_ID_REQUIRED",
        "SHOPPER_CREATING_SELLER_MISMATCH",
        "SHOPPER_ID_MISMATCH",
        "SHOPPER_ID_REQUIRED",
        "SHOPPER_IP_REQUIRED",
        "SKRILL_PROCESSING_FAILURE",
        "SKU_NOT_FOUND",
        "SUBSCRIPTION_CHARGE_NOT_FOUND",
        "SUBSCRIPTION_ID_REQUIRED",
        "SUBSCRIPTION_NOT_FOUND",
        "SWITCH_PLAN_ERROR",
        "TOO_MANY_PAYMENT_METHODS_SELECTED",
        "UNKNOWN_COUNTRY_CODE",
        "UNKNOWN_COUNTRY_FOR_IP_ADDRESS",
        "UNKNOWN_CURRENCY",
        "UNKNOWN_STATE_CODE",
        "UNKNOWN_STATE_FOR_IP_ADDRESS",
        "UPDATE_SELLER_ID_NOT_ALLOWED",
        "UPDATE_SUBSCRIPTION_FAILED",
        "VAT_VALIDATOR_GENERAL_FAILURE",
        "VENDOR_INSUFFICIENT_FUNDS_FOR_REFUND",
        
    ],

    "$risky": [
        "XSS_EXCEPTION",
        "ACCOUNT_CLOSED",
        "DO_NOT_HONOR",
        "HIGH_RISK_ERROR",
        "SHOPPER_COUNTRY_OFAC_SANCTIONED"
    ],


    
}
    final_sift_category = code
    for sift_category, bluesnap_categories in decline_category_dict.items():
        if code in bluesnap_categories:
            final_sift_category = sift_category
            return final_sift_category
    

    return final_sift_category
            
def get_status(estatus):
    match estatus: 
        case "Tx Exitosa":
            return "$success"
        case "Tx Fallida":
            return "$failure"
        case _: 
            return "$pending"


def main(): 

    #connection = psycopg2.connect(
    #    host='fw.payco.net.ve', 
    #    database='luka_calidad', 
    #    user='rmadonna', 
    #    password='6WLb@R^WNCXSeE', 
    #    port =  54320)
    
    connection = psycopg2.connect(
        host = 'lukadb.payco.net.ve',
        port = 54320, 
        database = 'luka', 
        user = 'rmadonna',
        password = 'XFZkwnk7JGHhjW')
    


    cursor = connection.cursor()

    query = """
        select distinct 
        t.id as "Id",                                           -- 0
        t.ip,                                                   -- 1
        (t.fecha_creacion at time zone 'vet') as "Fecha",       -- 2
        mon.codigo as "Moneda",                                 -- 3
        t.monto as "Monto",                                     -- 4
        t.email_tarjetahabiente as "Email",                     -- 5
        t.nombre_pagador as "Nombre",                           -- 6 
        e.descripcion as "Estatus",                             -- 7
        m.nombre_comercial as "Marca",                          -- 8
        mer.nombre as "Payment Method",                         -- 9
        t.tarjeta,                                              -- 10
        tp.nombre as "Tipo Pago",                               -- 11
        p.codigo_iso3166 as "Codigo Pais",                      -- 12
        t.respuesta_bluesnap as "Respuesta Bluesnap",           -- 13
        m.id as "ID Marca"                                      -- 14
        from transaccion t
        inner join servicio s on s.id=t.id_servicio
        inner join estatus e on e.id=t.id_estatus
        inner join pais p  on p.id=t.id_pais
        inner join sucursal su on su.id=s.id_sucursal
        inner join marca m on m.id=su.id_marca
        inner join moneda mon on mon.id=t.id_moneda
        inner join merchant mer on mer.id=t.id_merchant
        inner join tipo_pago tp on tp.id=t.id_tipo_pago
        where t.id_merchant=1  
        and t.id_estatus in (6,7,18)                          
        and t.fecha_creacion at time zone 'vet' between '2023-01-01 00:00:00' and '2023-12-31 23:59:59'
        order by 1
        limit 5
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print(rows[0])
    for x in range(0,len(rows[0])): 
        print(f"{x} -- {rows[0][x]}")

    #json_creation_transaction(rows)

    #json_creation_create_order(rows)


main()
