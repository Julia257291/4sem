
def main():
    function = get_function()
    method = get_metod()
    f = function["f"]
    interval = get_interval(f) #Tablica 0 - start, 1 - end
    stop_condition = get_stopcondition() # Mamy integer 1-2
    epsilon = get_value(stop_condition)

