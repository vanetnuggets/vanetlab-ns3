from ns import ns

# unsupported: ad
# supported: a, ac, b, g, n, 

def stdn(x):
    return '802.11' + x

def get_wifi_standard(standard):

    if standard == stdn('a'):
        return ns.wifi.WIFI_STANDARD_80211a

    elif standard == stdn('ac'):
        return ns.wifi.WIFI_STANDARD_80211ac
    
    elif standard == stdn('b'):
        return ns.wifi.WIFI_STANDARD_80211b
    
    elif standard == stdn('g'):
        return ns.wifi.WIFI_STANDARD_80211g
    
    elif standard == stdn('n'):
        return ns.wifi.WIFI_STANDARD_80211n
    
    elif standard == stdn('ax'):
        return ns.wifi.WIFI_STANDARD_80211ax
    
    elif standard == stdn('be'):
        return ns.wifi.WIFI_STANDARD_80211be
    
    elif standard == stdn('p'):
        return ns.wifi.WIFI_STANDARD_80211p

    return None
    # TODO finish this dogshit ...
