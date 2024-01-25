import sift

client = sift.Client(api_key='{apiKey}', account_id='{accountId}')


properties = {

    "$type" : "$transaction", 
    "$api_key" : "", #***************
    "$user_id"          : TX[5],
    "$amount"           : int(float(TX[4])*1000000), # $506.79
    "$currency_code"    : "USD",


    "$user_email"                : TX[5],
    "$decline_category"          : decline_category(TX[13]),
    "$order_id"                  : TX[0],
    "$transaction_id"            : TX[0],
    "$transaction_status" : TX[7],
    "$ip" : TX[1],
    "$time" : TX[2].timestamp(), 

    "$payment_method"   : {
        "$payment_type"    : TX[11], #*********************
        "$payment_gateway" : "$bluesnap", #*****************
        "$account_holder_name" : TX[6],
        "$card_bin"        : get_card_info(TX[10], True),
        "$card_last4"      : get_card_info(TX[10], False),
  },

}

response = client.track("$transaction", properties)