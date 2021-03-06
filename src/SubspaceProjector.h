// Copyright (c) 2017, Lawrence Livermore National Security, LLC and
// UT-Battelle, LLC.
// Produced at the Lawrence Livermore National Laboratory and the Oak Ridge
// National Laboratory.
// Written by J.-L. Fattebert, D. Osei-Kuffuor and I.S. Dunn.
// LLNL-CODE-743438
// All rights reserved.
// This file is part of MGmol. For details, see https://github.com/llnl/mgmol.
// Please also read this link https://github.com/llnl/mgmol/LICENSE

#ifndef MGMOL_SUBSPACEPROJ_H
#define MGMOL_SUBSPACEPROJ_H

#include "global.h"
#include "SquareLocalMatrices.h"

class ProjectedMatricesInterface;

template<class T>
class SubspaceProjector
{
private:
    T& subspace_;
    ProjectedMatricesInterface& proj_matrices_;
    short chromatic_number_;
    short subdivx_;
    int lda_;
    int loc_numpt_;

public:
    SubspaceProjector(T& subspace);

    ~SubspaceProjector() {}

    void projectOut(T&, SquareLocalMatrices<MATDTYPE>* mask = 0);
};

#endif
