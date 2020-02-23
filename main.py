import numpy as np
import pandas as pd
import os
import collections


def read_input(path, order_books_in_lib=True):
    f = open(path, 'r')
    first = f.readline()[:-1]
#     print(first)
    num_books, num_libs, num_days = first.split(' ')
    num_books, num_libs, num_days = int(num_books), int(num_libs), int(num_days)
    
    second = f.readline()[:-1]
    scores = list( map(lambda x: int(x), second.split(' ')) )
    
    lib_df = None
    books_dict = collections.OrderedDict()
    library_id = 0
    for library in range(num_libs):
        first = f.readline()[:-1]
        num_books_inlib, num_days_signup, books_per_day = first.split(' ')
        num_books_inlib, num_days_signup, books_per_day = int(num_books_inlib), int(num_days_signup), int(books_per_day)
        
        second = f.readline()[:-1]
        books_inlib = list( map(lambda x: int(x), second.split(' ')) )
        
        d={'num_books_inlib' : [num_books_inlib], 'num_days_signup' : [num_days_signup], 'books_per_day' : [books_per_day]}
        lib_df = pd.DataFrame(data=d) if lib_df is None else pd.concat([lib_df, pd.DataFrame(data=d)], ignore_index=True)
        
        if order_books_in_lib:
            books_inlib.sort(key=lambda x: scores[x], reverse=True)

        books_dict[library_id] = np.array(books_inlib)
        library_id += 1
    
    return num_books, scores, num_libs, num_days, lib_df, books_dict


# +
input_path = 'a.txt'
num_books, scores, num_libs, num_days, lib_df, books_in_lib = read_input(input_path)

print('Total number of books:', num_books)
print('Total number of libraries:', num_libs)
print('Total number of days:', num_days)
print('Scores:', scores)
print('Libraries df:', lib_df)
print('Books in libraries df:', books_in_lib)
# -


lib_df


def get_library_score_and_books(lib,n,books_in_lib, scores):
    if  n-lib.num_days_signup < 0:
        return 0, []
    expected_books = min((n-lib.num_days_signup)*lib.books_per_day,len(books_in_lib[lib.id]))
    
    books = books_in_lib[lib.id][:expected_books]
    #print('-.-.-',expected_books,books,len(books_in_lib[lib.id]), (n-lib.num_days_signup)*lib.books_per_day)
    return (sum([scores[b] for b in books]), books)


def update_libraries_books(books_in_lib, selected_books):
    books_in_lib_2 = books_in_lib.copy()
    for key, values in books_in_lib.items():
        books_in_lib_2[key]=[item for item in values if item not in selected_books]
        #print(values, books_in_lib_2[key], selected_books, (n-lib.num_days_signup)*lib.books_per_day+1, len(books_in_lib[lib.id]))
    return books_in_lib_2


def schedule(path):
    i=0
    num_books, scores, num_libs, num_days, lib_df, books_in_lib = read_input(path)
    lib_df.index.name='id'
    lib_df = lib_df.reset_index()
    final_books = []
    while i < num_days and len(lib_df)!=0:
        print(i, len(lib_df))
        scores_and_books = lib_df.apply(partial(get_library_score_and_books, n=num_days-i, books_in_lib=books_in_lib, scores=scores),axis=1)
#         print(scores_and_books, i)
        lib_df['score']=scores_and_books.apply(lambda x:x[0])
        lib_df['books']=scores_and_books.apply(lambda x:x[1])
        lib_selected = lib_df.sort_values('score', ascending=False).iloc[0]
        if lib_selected.score != 0:
            books_selected = lib_selected['books']
#             print('hem escollit ',lib_selected.id, books_selected)
        
            lib_df = lib_df[lib_df['id']!=lib_selected.id].copy()

            final_books.append((lib_selected.id,books_selected.copy()))
            del books_in_lib[lib_selected.id]
#             print(books_selected)
            books_in_lib = update_libraries_books(books_in_lib, books_selected)
#             print(books_in_lib)
            i+=lib_selected.num_days_signup
        else:
            i+=1
#         print(len(lib_df))
    return final_books


schedule('a.txt')

result_b = schedule('b.txt')

result_c = schedule('c.txt')

num_books, scores_c, num_libs, num_days, lib_df, books_in_lib = read_input('c.txt')


sum([sum([scores_c[book] for book in books]) for lib, books in result_c])

num_books, scores_b, num_libs, num_days, lib_df, books_in_lib = read_input('b.txt')

sum([sum([scores_b[book] for book in books]) for lib, books in result_b])

result_e = schedule('e.txt')

num_books, scores_f, num_libs, num_days, lib_df, books_in_lib = read_input('f.txt')


def write_output(name,llista):
    with open(name, 'w') as f:
        f.write(str(len(llista))+'\n')
        for lib, books in llista:
            f.write(str(lib)+' ')
            f.write(str(len(books))+'\n')
            for book in books:
                f.write(str(book)+' ')
            f.write('\n')


write_output('e_sol.txt',result_e)


def update_libraries_books(books_in_lib, selected_books):
    books_in_lib_2 = books_in_lib.copy()
    for key, values in books_in_lib.items():
        books_in_lib_2[key]=[item for item in values if item not in selected_books]
        #print(values, books_in_lib_2[key], selected_books, (n-lib.num_days_signup)*lib.books_per_day+1, len(books_in_lib[lib.id]))
    return books_in_lib_2


collections.OrderedDict([(1, array([3, 5, 2, 0]))]), []
