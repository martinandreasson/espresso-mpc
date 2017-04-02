#!/usr/bin/python

def mpc_matrices(tempc, T_s):

    import math
    import config as conf
    import numpy
    from scipy import linalg
    from cvxopt import matrix

    n = conf.n
    dt = conf.sample_time
    steam_state = False

    ## MPC ##
    # System matrices for different dt
    B = numpy.mat([[conf.a_1*conf.c_u*dt],[0]])

    dt = dt*5
    B_2 = numpy.mat([[conf.a_1*conf.c_u*dt],[0]])

    dt = dt*5
    B_3 = numpy.mat([[conf.a_1*conf.c_u*dt],[0]])

    dt = conf.sample_time
    A = numpy.mat([[1 - conf.a_1*dt*conf.c_1, conf.a_1*dt*conf.c_1], [conf.a_1*dt*conf.c_1, 1 - conf.a_1*dt*conf.c_1 - conf.a_1*4*conf.c_2*dt*(tempc + 273)**3]])
    B2 = numpy.mat([[0],[conf.a_1*conf.c_2*dt*((T_s + 273)**4 - (tempc + 273)**4) - conf.a_1*conf.c_2*dt*4*(tempc + 273)**3*(0)]])

    dt = dt*5
    A_2 = numpy.mat([[1 - conf.a_1*dt*conf.c_1, conf.a_1*dt*conf.c_1], [conf.a_1*dt*conf.c_1, 1 - conf.a_1*dt*conf.c_1 - conf.a_1*4*conf.c_2*dt*(tempc + 273)**3]])
    B2_2 = numpy.mat([[0],[conf.a_1*conf.c_2*dt*((T_s + 273)**4 - (tempc + 273)**4) - conf.a_1*conf.c_2*dt*4*(tempc + 273)**3*(0)]])

    dt = dt*5
    A_3 = numpy.mat([[1 - conf.a_1*dt*conf.c_1, conf.a_1*dt*conf.c_1], [conf.a_1*dt*conf.c_1, 1 - conf.a_1*dt*conf.c_1 - conf.a_1*4*conf.c_2*dt*(tempc + 273)**3]])
    B2_3 = numpy.mat([[0],[conf.a_1*conf.c_2*dt*((T_s + 273)**4 - (tempc + 273)**4) - conf.a_1*conf.c_2*dt*4*(tempc + 273)**3*(0)]])

    A_app = numpy.zeros(shape=(2*n,2))
    A_tmp = numpy.identity(2)
    for i in range(0,2*n,2):
        if i < 5:
            A_tmp = A*A_tmp
        elif i < 10:
            A_tmp = A_2*A_tmp
        else:
            A_tmp = A_3*A_tmp

        A_app[i,0] = A_tmp[0,0]
        A_app[i,1] = A_tmp[0,1]
        A_app[i+1,0] = A_tmp[1,0]
        A_app[i+1,1] = A_tmp[1,1]

    AB_app = numpy.zeros(shape=(2*n,n))

    for i in range(0,n):

        for j in range(0,i):

            if j < 5:
                B_tmp = B
            elif j < 10:
                B_tmp = B_2
            else:
                B_tmp = B_3

            exp_1 = i - j
            if exp_1 < 0:
                exp_1 = 0
            elif exp_1 > 4:
                exp_1 = 4

            exp_2 = i - j - 5
            if exp_2 < 0:
                exp_2 = 0
            elif exp_2 > 4:
                exp_2 = 4

            exp_3 = i - j - 10
            if exp_3 < 0:
                exp_3 = 0

            AB_tmp = A_3**exp_3*A_2**exp_2*A**exp_1*B_tmp
            AB_app[2*i:2*i+2,j] = AB_tmp.ravel()

    AB_2app = numpy.zeros(shape=(2*n,n))

    for i in range(0,n):

        for j in range(0,i):

            if j < 5:
                B2_tmp = B2
            elif j < 10:
                B2_tmp = B2_2
            else:
                B2_tmp = B2_3

            exp_1 = i - j
            if exp_1 < 0:
                exp_1 = 0
            elif exp_1 > 4:
                exp_1 = 4

            exp_2 = i - j - 5
            if exp_2 < 0:
                exp_2 = 0
            elif exp_2 > 4:
                exp_2 = 4

            exp_3 = i - j - 10
            if exp_3 < 0:
                exp_3 = 0

            AB_2tmp = A_3**exp_3*A_2**exp_2*A**exp_1*B2_tmp
            AB_2app[2*i:2*i+2,j] = AB_2tmp.ravel()

    I_mod = numpy.zeros(shape=(n,2*n))
    for i in range(0,n):
        I_mod[i, 2*i+1] = 1

    # Cost function
    q1 = numpy.zeros((3*n,1))
    q2 = numpy.ones((n,1))
    q = numpy.vstack((q1, q2))

    # Optimization block matrices
    d_1vec_zeros = numpy.zeros((n,1))
    d_1vec_ones = -numpy.ones((n,1))*conf.brew_boost

    # Temperature disturbance
    d_2vec = numpy.ones(shape=(n,1))

    # Equality constraint
    A_constr = numpy.concatenate((numpy.identity(2*n), -AB_app, numpy.zeros((2*n,n))), axis=1)
    b_constr = numpy.matrix(AB_app)*numpy.matrix(d_1vec_zeros) + numpy.dot(AB_2app, d_2vec)
    b_constr_brew = numpy.matrix(AB_app)*numpy.matrix(d_1vec_ones) + numpy.dot(AB_2app, d_2vec)

    # Inequality constraint
    G1 = numpy.concatenate((numpy.zeros((n,2*n)), numpy.identity(n), numpy.zeros((n,n))), axis=1)
    G2 = numpy.concatenate((numpy.zeros((n,2*n)), -numpy.identity(n), numpy.zeros((n,n))), axis=1)
    G3 = numpy.concatenate((I_mod, numpy.zeros((n,n)), -numpy.identity(n)), axis=1)
    G4 = numpy.concatenate((-I_mod, numpy.zeros((n,n)), -numpy.identity(n)), axis=1)
    G = numpy.vstack((G1, G2, G3, G4))

    h1 = 100*numpy.ones((n,1))
    h2 = numpy.zeros((n,1))
    h3 = numpy.zeros((n,1))
    h4 = numpy.zeros((n,1))
    h = numpy.vstack((h1, h2, h3, h4))

    # Optimization matrices
    q_opt = matrix(q, tc='d')
    G_opt = matrix(G, tc='d')
    h_opt = matrix(h, tc='d')
    A_opt = matrix(A_constr, tc='d')

    # Return matrices
    return {'q_opt': q_opt, 'G_opt': G_opt, 'h_opt': h_opt, 'A_opt': A_opt, 'b_constr': b_constr, 'b_constr_brew': b_constr_brew, 'A': A, 'B': B, 'B2': B2, 'A_app': A_app}
