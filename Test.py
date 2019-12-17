number = [
'0984705474'
,'0936055858'
,'0383104055'
,'0383104055'
,'0984705474'
,'0936055858'
,'0974971842'
,'0936055858'
,'0984705474'
,'0383104055'
          ]

import requests
from multiprocessing.dummy import Pool

import requests

pool = Pool(10) # Creates a pool with ten threads; more threads = more concurrency.
                # "pool" is a module attribute; you can be sure there will only
                # be one of them in your application
                # as modules are cached after initialization.

if __name__ == '__main__':
    futures = []
    for n in number:
        futures.append(pool.apply_async(requests.get, ['http://127.0.0.1:5000/getavatar?phone=' + n]))
    # futures is now a list of 10 futures.
    for future in futures:
        print(future.get().text)
        print('----------------------------------')