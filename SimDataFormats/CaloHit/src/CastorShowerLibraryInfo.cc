#include "SimDataFormats/CaloHit/interface/CastorShowerLibraryInfo.h"
#include <iostream>

CastorShowerLibraryInfo::CastorShowerLibraryInfo() {
  // Clear();
  // std::cout << "\n    *** CastorShowerLibraryInfo object created ***    " << std::endl;
}

CastorShowerLibraryInfo::~CastorShowerLibraryInfo() {}

void CastorShowerLibraryInfo::Clear(Option_t* option) {
  Energy.Clear();
  Eta.Clear();
  Phi.Clear();
}
