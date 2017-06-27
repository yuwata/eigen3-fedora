# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%global commit b4f969795d1b
%{?commit:%global commitshort %(c=%{commit}; echo ${c:0:7})}

Name:           eigen3
Version:        3.3.4
Release:        1.2%{?commit:.hg%{commitshort}}%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math

Group:          Development/Libraries
License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
%if %{defined commit}
Source0:        http://bitbucket.org/eigen/eigen/get/%{commit}.tar.bz2
%else
Source0:        http://bitbucket.org/eigen/eigen/get/%{version}.tar.bz2
%endif

# Install FindEigen3.cmake
# Adapted from Debian eigen3 package
Patch0:         01_install_FindEigen3.patch

# Fix pkg-config file
Patch1:         eigen_pkgconfig.patch
# Fix the include paths in the new Eigen3Config.cmake file
Patch2:         eigen3-3.3.1-fixcmake.patch

BuildRequires:  atlas-devel
BuildRequires:  fftw-devel
BuildRequires:  glew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
BuildRequires:  sparsehash-devel
BuildRequires:  suitesparse-devel
BuildRequires:  gcc-gfortran
BuildRequires:  SuperLU-devel
BuildRequires:  qt-devel
BuildRequires:  scotch-devel
BuildRequires:  metis-devel

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  tex(latex)

%description
%{summary}.

%package devel
Summary:   A lightweight C++ template library for vector and matrix math
Group:     Development/Libraries
BuildArch: noarch
# -devel subpkg only atm, compat with other distros
Provides:  %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:  %{name}-static = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary:   Developer documentation for Eigen
Requires:  %{name}-devel = %{version}-%{release}
BuildArch: noarch
%description doc
Developer documentation for Eigen.

%prep
%setup -q -n eigen-eigen-%{commit}
%patch0 -p1
%patch1 -p1
%patch2 -p0 -b .fixcmake
%build
mkdir %{_target_platform}
pushd %{_target_platform}
#%ifarch ppc64
# Currently get a compiler ICE, work around it
# https://bugzilla.redhat.com/show_bug.cgi?id=1063999
#export CXXFLAGS="%{optflags} -mno-vsx"
#%endif
%cmake .. -DINCLUDE_INSTALL_DIR=%{_includedir}/eigen3 \
  -DBLAS_LIBRARIES="cblas" \
  -DSUPERLU_INCLUDES=%{_includedir}/SuperLU \
  -DSCOTCH_INCLUDES=%{_includedir} -DSCOTCH_LIBRARIES="scotch" \
  -DMETIS_INCLUDES=%{_includedir} -DMETIS_LIBRARIES="metis" \
  -DCMAKEPACKAGE_INSTALL_DIR=%{_datadir}/%{name}
popd
%make_build -C %{_target_platform}
%make_build doc -C %{_target_platform}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
%make_install -C %{_target_platform}

%check
# Run tests but make failures non-fatal. Note that upstream doesn't expect the
# tests to pass consistently since they're seeded randomly.
#make -C %{_target_platform} %{?_smp_mflags} buildtests
#make -C %{_target_platform} %{?_smp_mflags} test ARGS="-V" || exit 0

%files devel
%license COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%{_includedir}/eigen3
%{_datadir}/%{name}
%{_datadir}/pkgconfig/*
%{_datadir}/cmake/Modules/*.cmake

%files doc
%doc %{_target_platform}/doc/html

%changelog
* Tue Jun 27 2017 Yu Watanabe <watanabe.yu@gmail.com> - 3.3.4-1.2.hgb4f9697
- Update to latest snapshot b4f969795d1b

* Wed Jun 21 2017 Yu Watanabe <watanabe.yu@gmail.com> - 3.3.4-1.1.hg211bfd9
- Update to latest snapshot 211bfd92504a

* Mon Jun 19 2017 Sandro Mani <manisandro@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Wed Feb 22 2017 Sandro Mani <manisandro@gmail.com> - 3.3.3-1
- Update to 3.3.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Sandro Mani <manisandro@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Wed Dec 28 2016 Rich Mattes <richmattes@gmail.com> - 3.3.1-1
- Update to 3.3.1 (rhbz#1408538)

* Wed Nov 23 2016 Rich Mattes <richmattes@gmail.com> - 3.3.0-1
- Update to 3.3.0
- Stop renaming tarball - just use upstream tarball

* Tue Oct 04 2016 Sandro Mani <manisandro@gmail.com> - 3.2.10-1
- Update to 3.2.10

* Tue Jul 19 2016 Sandro Mani <manisandro@gmail.com> - 3.2.9-1
- Update to 3.2.9

* Sat Feb 20 2016 Sandro Mani <manisandro@gmail.com> - 3.2.8-1
- Update to 3.2.8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-3
- Again: Fix incorrect include path in pkgconfig file

* Fri Nov 06 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-2
- Fix incorrect include path in pkgconfig file

* Thu Nov 05 2015 Sandro Mani <manisandro@gmail.com> - 3.2.7-1
- Update to release 3.2.7

* Thu Oct 01 2015 Sandro Mani <manisandro@gmail.com> - 3.2.6-1
- Update to release 3.2.6

* Fri Aug 21 2015 Rich Mattes <richmattes@gmail.com> - 3.2.5-2
- Apply patch to install FindEigen3.cmake

* Tue Jun 16 2015 Sandro Mani <manisandro@gmail.com> - 3.2.5-1
- Update to release 3.2.5

* Thu Jan 22 2015 Sandro Mani <manisandro@gmail.com> - 3.2.4-1
- Update to release 3.2.4

* Mon Jan 05 2015 Rich Mattes <richmattes@gmail.com> - 3.2.3-2
- Backport upstream Rotation2D fix

* Thu Dec 18 2014 Sandro Mani <manisandro@gmail.com> - 3.2.3-1
- Update to release 3.2.3
- Drop upstreamed eigen3-ppc64.patch

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Sandro Mani <manisandro@gmail.com> - 3.2.2-1
- Update to release 3.2.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Add ppc64 support

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-3
- Make doc package noarch

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-2
- Split off doc to a separate package

* Wed Feb 26 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-1
- Udpate to release 3.2.1

* Sun Aug 11 2013 Sandro Mani <manisandro@gmail.com> - 3.2-3
- Build and run tests
- Drop -DBLAS_LIBRARIES_DIR, not used
- Add some BR to enable tests of corresponding backends
- spec cleanup

* Wed Jul 24 2013 Sandro Mani <manisandro@gmail.com> - 3.2-1
- Update to release 3.2

* Sat Jun 29 2013 Rich Mattes <richmattes@gmail.com> - 3.1.3-2
- Add upstream patch to fix malloc/free bugs (rhbz#978971)

* Fri Apr 19 2013 Sandro Mani <manisandro@gmail.com> - 3.1.3-1
- Update to release 3.1.3
- Add patch for unused typedefs warning with gcc4.8

* Tue Mar 05 2013 Rich Mattes <richmattes@gmail.com> - 3.1.2-1
- Update to release 3.1.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Tim Niemueller <tim@niemueller.de> - 3.0.6-1
- Update to release 3.0.6 (fixes GCC 4.7 warnings)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Rich Mattes <richmattes@gmail.com> - 3.0.5-1
- Update to release 3.0.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Rich Mattes <richmattes@gmail.com> - 3.0.4-1
- Update to release 3.0.4

* Tue Nov 15 2011 Rich Mattes <richmattes@gmail.com> - 3.0.3-1
- Update to release 3.0.3

* Sun Apr 17 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-2
- Patched sources to fix build failure
- Removed fixes made upstream
- Added project name to source tarball filename

* Sat Mar 26 2011 Rich Mattes <richmattes@gmail.com> - 3.0.0-1
- Update to release 3.0.0

* Tue Jan 25 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.2.beta2
- Change blas-devel buildrequirement to atlas-devel
- Don't make the built-in experimental blas library

* Mon Jan 24 2011 Rich Mattes <richmattes@gmail.com> - 3.0-0.1.beta2
- Initial package
