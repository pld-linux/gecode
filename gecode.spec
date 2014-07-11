# TODO
# - html docs seems not to be built

# Conditional build:
%bcond_with	doc		# build doc

Summary:	Generic constraint development environment
Name:		gecode
Version:	4.2.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.gecode.org/download/%{name}-%{version}.7z
# Source0-md5:	5a37a56647b1c593640ebd085bf4c066
Patch0:		no_examples.patch
URL:		http://www.gecode.org/
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	flex >= 2.5.33
BuildRequires:	graphviz
BuildRequires:	p7zip-standalone
BuildRequires:	qt4-build
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	tex(dvips)
BuildRequires:	tex(latex)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gecode is a toolkit for developing constraint-based systems and
applications. Gecode provides a constraint solver with
state-of-the-art performance while being modular and extensible.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package examples
Summary:	Example code for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
The %{name}-examples package contains example code for %{name}.

%prep
%setup -q
%patch0 -p1

# Fix permissions
find . -name '*.hh' -exec chmod 0644 '{}' \;
find . -name '*.hpp' -exec chmod 0644 '{}' \;
find . -name '*.cpp' -exec chmod 0644 '{}' \;
chmod 0644 LICENSE misc/doxygen/*.png

# Fix encoding
cd examples
for file in bin-packing.cpp black-hole.cpp dominating-queens.cpp scowl.hpp word-square.cpp; do
	iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
	touch -r $file $file.new && \
	mv $file.new $file
done

%build
%{__aclocal}
%{__autoconf}
%configure \
	--disable-examples \
	--enable-float-vars \
	--enable-leak-debug \
	--with-boost-include=%{_includedir}/boost

%{__make}
%{__make} doc
%{__make} ChangeLog

iconv --from=ISO-8859-1 --to=UTF-8 -o ChangeLog.new ChangeLog
mv ChangeLog.new ChangeLog

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE
%attr(755,root,root) %{_libdir}/libgecodedriver.so.*.*
%ghost %{_libdir}/libgecodedriver.so.36
%attr(755,root,root) %{_libdir}/libgecodeflatzinc.so.*.*
%ghost %{_libdir}/libgecodeflatzinc.so.36
%attr(755,root,root) %{_libdir}/libgecodefloat.so.*.*
%ghost %{_libdir}/libgecodefloat.so.36
%attr(755,root,root) %{_libdir}/libgecodegist.so.*.*
%ghost %{_libdir}/libgecodegist.so.36
%attr(755,root,root) %{_libdir}/libgecodeint.so.*.*
%ghost %{_libdir}/libgecodeint.so.36
%attr(755,root,root) %{_libdir}/libgecodekernel.so.*.*
%ghost %{_libdir}/libgecodekernel.so.36
%attr(755,root,root) %{_libdir}/libgecodeminimodel.so.*.*
%ghost %{_libdir}/libgecodeminimodel.so.36
%attr(755,root,root) %{_libdir}/libgecodesearch.so.*.*
%ghost %{_libdir}/libgecodesearch.so.36
%attr(755,root,root) %{_libdir}/libgecodeset.so.*.*
%ghost %{_libdir}/libgecodeset.so.36
%attr(755,root,root) %{_libdir}/libgecodesupport.so.*.*
%ghost %{_libdir}/libgecodesupport.so.36

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fzn-gecode
%attr(755,root,root) %{_bindir}/mzn-gecode
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_libdir}/libgecodedriver.so
%{_libdir}/libgecodeflatzinc.so
%{_libdir}/libgecodefloat.so
%{_libdir}/libgecodegist.so
%{_libdir}/libgecodeint.so
%{_libdir}/libgecodekernel.so
%{_libdir}/libgecodeminimodel.so
%{_libdir}/libgecodesearch.so
%{_libdir}/libgecodeset.so
%{_libdir}/libgecodesupport.so

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
