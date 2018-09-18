# NO IMPORTS ALLOWED!

import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    return any({actor_id_1, actor_id_2} == {id1, id2} for id1, id2, _ in data)

def get_actors_with_bacon_number(data, n, paths=False):
    bacon = 4724
    actors_w_bacon_num = {0: {bacon}}
    for i in range(1, n + 1):
        actors_w_bacon_num[i] = set() # initialize dict value 
        all_actors = set().union(*actors_w_bacon_num.values())

        for a1, a2, _ in data:
            if a1 in actors_w_bacon_num[i - 1] and a2 not in all_actors:
                actors_w_bacon_num[i].add(a2)
            if a2 in actors_w_bacon_num[i - 1] and a1 not in all_actors:
                actors_w_bacon_num[i].add(a1)
    return actors_w_bacon_num[n]

def get_bacon_path(data, actor_id):
    return get_path(data, 4724, actor_id)

def get_path(data, actor_id_1, actor_id_2):
    bacon = actor_id_1
    actors_w_bacon_num = {0: {bacon}}
    parent = {bacon: bacon}
    i = 1
    while True:
        actors_w_bacon_num[i] = set() # initialize dict value 
        all_actors = set().union(*actors_w_bacon_num.values())

        for a1, a2, _ in data:
            if a1 in actors_w_bacon_num[i - 1] and a2 not in all_actors:
                actors_w_bacon_num[i].add(a2)
                parent[a2] = a1
            if a2 in actors_w_bacon_num[i - 1] and a1 not in all_actors:
                actors_w_bacon_num[i].add(a1)
                parent[a1] = a2

        if actor_id_2 in actors_w_bacon_num[i]:
            break
        
        if len(actors_w_bacon_num[i]) == 0:
            return None
        
        i += 1

    path = [actor_id_2]
    while parent[path[-1]] != path[-1]:
        path.append(parent[path[-1]])
    return list(reversed(path))

def name2id(name):
    return namesdb[name]

def id2name(id_):
    return idsdb[id_]

def id2movie(id_):
    return moviesreversedb[id_]

def get_movie_path(data, path):
    actor_movie_db = dict()
    for a1, a2, movieid in data:
        actor_movie_db[(a1, a2)] = movieid
        actor_movie_db[(a2, a1)] = movieid

    moviepath = []
    for i in range(1, len(path)):
        moviepath.append(actor_movie_db[(path[i - 1], path[i])])
        
    return moviepath

if __name__ == '__main__':
    with open('resources/names.json') as f:
        global namesdb, idsdb
        namesdb = json.load(f)
        # create a reversible dictionary mapping
        idsdb = dict()
        for k, v in namesdb.items():
            idsdb[v] = k
    
    with open('resources/movies.json') as f:
        global moviesdb, moviesreversedb
        moviesdb = json.load(f)
        moviesreversedb = dict()
        for k, v in moviesdb.items():
            moviesreversedb[v] = k

    with open('resources/tiny.json') as f:
        tinydb = json.load(f)

    with open('resources/small.json') as f:
        smalldb = json.load(f)

    with open('resources/large.json') as f:
        largedb = json.load(f)
    
    # print(did_x_and_y_act_together(smalldb, name2id("Phil Hartman"), name2id("David Morse")))
    # print(did_x_and_y_act_together(smalldb, name2id("Sten Hellstrom"), name2id("Mats Ingerdal")))
    # print(did_x_and_y_act_together(smalldb, name2id("Lew Knopp"), name2id("Daphne Rubin-Vega")))
    # print(did_x_and_y_act_together(smalldb, name2id("Charles Berling"), name2id("Robert Viharo")))
    # print(get_actors_with_bacon_number(tinydb, 0))
    # print(get_actors_with_bacon_number(tinydb, 1))
    # print(get_actors_with_bacon_number(tinydb, 2))
    # print(list(map(id2name, get_actors_with_bacon_number(smalldb, 3))))
    # print(get_actors_with_bacon_number(smalldb, 4))
    # print(list(map(id2name, get_actors_with_bacon_number(largedb, 5))))
    # print(list(map(id2name, get_actors_with_bacon_number(largedb, 6))))
    # print(get_bacon_path(tinydb, 46866))
    # print(list(map(id2name, get_bacon_path(largedb, name2id("Toby Jones")))))
    # print(list(map(id2name, get_bacon_path(largedb, name2id("Mikijiro Hira")))))
    # print(list(map(id2name, get_bacon_path(largedb, name2id("Anton Radacic")))))
    # print(list(map(id2name, get_path(largedb, name2id("Christina Ricci"), name2id("Anton Radacic")))))
    # print(list(map(id2name, get_path(largedb, name2id("Al Hallett"), name2id("Robert Duvall")))))
    print(list(map(id2movie, get_movie_path(largedb, get_path(largedb, name2id("Sven Batinic"), name2id("Jean Speegle Howard"))))))
    print(list(map(id2movie, get_movie_path(largedb, get_path(largedb, name2id("Bruce McGill"), name2id("Mick Blue"))))))

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
