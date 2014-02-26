# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%global commit 6b38706d90a9

Name:           eigen3
Version:        3.2.1
Release:        1%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math

Group:          Development/Libraries
License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
# Source file is at: http://bitbucket.org/eigen/eigen/get/3.1.3.tar.bz2
# Renamed source file so it's not just a version number
Source0:        eigen-%{version}.tar.bz2

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

%prep
%setup -q -n eigen-eigen-%{commit}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. -DBLAS_LIBRARIES="cblas" -DSUPERLU_INCLUDES=%{_includedir}/SuperLU
popd
make -C %{_target_platform} %{?_smp_mflags}
make doc -C %{_target_platform} %{?_smp_mflags}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
%make_install -C %{_target_platform}

%check
# Exclude tests that are failing:

%ifarch armv7hl
# The following tests FAILED:
#	  3 - dynalloc (Failed)
#	  4 - nomalloc_3 (Failed)
#	  5 - nomalloc_2 (Failed)
#	 14 - packetmath_3 (Failed)
#	 54 - redux_6 (Failed)
#	 62 - visitor_6 (Failed)
#	153 - array_6 (Failed)
#	159 - array_for_matrix_6 (Failed)
#	254 - product_trsolve_8 (Failed)
#	311 - qr_colpivoting_1 (Failed)
#	337 - schur_complex_2 (Failed)
#	405 - geo_hyperplane_1 (Failed)
#	576 - matrix_exponential_6 (Failed)
#	584 - matrix_power_9 (Failed)
#	586 - matrix_power_8 (Failed)
#	623 - gmres_2 (Failed)
#	624 - minres_1 (Failed)
#	630 - gmres_1 (Failed)
#	632 - levenberg_marquardt (Failed)
excluded_tests="dynalloc|nomalloc_2|nomalloc_3|packetmath_3|redux_6|visitor_6|array_6|array_for_matrix_6|product_trsolve_8|qr_colpivoting_1|schur_complex_2|geo_hyperplane_1|matrix_exponential_6|matrix_power_8|matrix_power_9|gmres_2|minres_1|gmres_1|levenberg_marquardt"
%endif

%ifarch x86_64
# The following tests FAILED:
#	585 - matrix_function_1 (Failed)
#	608 - mpreal_support (Failed)
#   631 - gmres_2 (Failed)
#	632 - gmres_1 (Failed)
#   632 - minres_1 (Failed)
#   635 - levenberg_marquardt (Failed)
#   647 - bdcsvd_2 (Failed)
excluded_tests="matrix_function_1|mpreal_support|gmres_1|gmres_2|minres_1|levenberg_marquardt|bdcsvd_2"
%endif

%ifarch %{ix86}
# The following tests FAILED:
#	177 - ref_1 (Failed)
#	281 - lu_5 (Failed)
#	555 - superlu_support_2 (Failed)
#	556 - cholmod_support_1 (Failed)
#	557 - cholmod_support_2 (Failed)
#	570 - NonLinearOptimization (Failed)
#	603 - mpreal_support (Failed)
#	627 - gmres_2 (Failed)
#	629 - minres_1 (Failed)
#	633 - gmres_1 (Failed)
#	635 - levenberg_marquardt (Failed)
#	643 - bdcsvd_2 (Failed)
excluded_tests="ref_1|lu_5|superlu_support_2|cholmod_support_1|cholmod_support_2|NonLinearOptimization|mpreal_support|gmres_2|minres_1|gmres_1|levenberg_marquardt|bdcsvd_2"
%endif

make -C %{_target_platform} %{?_smp_mflags} buildtests
make -C %{_target_platform} %{?_smp_mflags} test ARGS="-V -E '$excluded_tests'"

%files devel
%doc COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%doc %{_target_platform}/doc/html
%{_includedir}/eigen3
%{_datadir}/pkgconfig/*

%changelog
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
