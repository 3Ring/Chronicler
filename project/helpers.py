def validate(var, name, it=0):
    strit=str(it)
    print((it+1)*5*'{0}'.format(it), '<><><><>', (50-it)*'{0}'.format(it))
    print('\n', name, ': ', '<'+strit+'<'+strit+'<'+strit+'<', var, '>'+strit+'>'+strit+'>'+strit+'>', '\n', 'Is type: ', type(var), '\n')
    print(10*('-'+strit)+'-')
    try:
        if len(var) > 1:
            it+=1
            strit=str(it)
            print((it+1)*3*'{0}'.format(it), '<><><><>', (30-it)*'{0}'.format(it))
            for item in var:
                try:
                    if len(item) > 1:
                        validate(item, "recur-item<{0}>".format(it), it)
                except:
                    print('\n', name, ': ', '<'+strit+'<'+strit+'<'+strit+'<', item, '>'+strit+'>'+strit+'>'+strit+'>', '\n', 'Is type: ', type(item), '\n')
        
        return None
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return None