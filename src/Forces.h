// Copyright (c) 2017, Lawrence Livermore National Security, LLC and
// UT-Battelle, LLC.
// Produced at the Lawrence Livermore National Laboratory and the Oak Ridge
// National Laboratory.
// Written by J.-L. Fattebert, D. Osei-Kuffuor and I.S. Dunn.
// LLNL-CODE-743438
// All rights reserved.
// This file is part of MGmol. For details, see https://github.com/llnl/mgmol.
// Please also read this link https://github.com/llnl/mgmol/LICENSE

#ifndef MGMOL_FORCES_H
#define MGMOL_FORCES_H

#include "Hamiltonian.h"
#include "Rho.h"
#include "global.h"

#define NPTS 2
#define DELTAC 0.002

class Ion;
class Ions;
class ProjectedMatricesInterface;

template <class T>
class Forces
{
private:
    Hamiltonian<T>* hamiltonian_;
    Rho<T>* rho_;
    ProjectedMatricesInterface* proj_matrices_;

    static Timer lforce_tm_;
    static Timer nlforce_tm_;
    static Timer get_var_tm_;
    static Timer get_loc_proj_tm_;
    static Timer consolidate_data_;
    static Timer lforce_local_tm_;
    static Timer kbpsi_tm_;
    static Timer energy_tm_;
    static Timer total_tm_;

    void lforce_ion(Ion& ion, RHODTYPE* rho, double** loc_proj);
    void get_loc_proj(RHODTYPE* rho, const int* const pvec, double*** var_pot,
        double*** var_charge, const int docount, double** loc_proj);
    int get_var(Ion& ion, int* pvec, double*** var_pot, double*** var_charge);

public:
    Forces(Hamiltonian<T>* hamiltonian, Rho<T>* rho,
        ProjectedMatricesInterface* proj_matrices)
        : hamiltonian_(hamiltonian), rho_(rho), proj_matrices_(proj_matrices)
    {
        assert(hamiltonian_ != 0);
        assert(rho_ != 0);
        assert(proj_matrices_ != 0);
    }

    void nlforce(T& orbitals, Ions& ions);
    void nlforceSparse(T& orbitals, Ions& ions);
    void lforce(Ions& ions, RHODTYPE* rho);
    void force(T& orbitals, Ions& ions);

    void printTimers(ostream& os)
    {
        lforce_tm_.print(os);
        nlforce_tm_.print(os);
        get_var_tm_.print(os);
        get_loc_proj_tm_.print(os);
        consolidate_data_.print(os);
        lforce_local_tm_.print(os);
        kbpsi_tm_.print(os);
        energy_tm_.print(os);
        total_tm_.print(os);
    }
};

template <class T>
Timer Forces<T>::lforce_tm_("Forces::lforce");
template <class T>
Timer Forces<T>::nlforce_tm_("Forces::nlforce");
template <class T>
Timer Forces<T>::get_var_tm_("Forces::var");
template <class T>
Timer Forces<T>::get_loc_proj_tm_("Forces::loc_proj");
template <class T>
Timer Forces<T>::consolidate_data_("Forces::consolidate");
template <class T>
Timer Forces<T>::lforce_local_tm_("Forces::lforce_local");
template <class T>
Timer Forces<T>::total_tm_("Forces::total");
template <class T>
Timer Forces<T>::kbpsi_tm_("Forces::KBpsi");
template <class T>
Timer Forces<T>::energy_tm_("Forces::nl_energy");

#endif
