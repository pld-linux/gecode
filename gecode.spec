# TODO
# - html docs seems not to be built

# Conditional build:
%bcond_with	doc		# build doc
%bcond_without	qt		# Qt support (qt4>4.3, qt5)
%bcond_without	gist	# Gecode Interactive Search Tool

%if %{without qt}
%undefine	with_gist
%endif

Summary:	Generic constraint development environment
Name:		gecode
Version:	4.4.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.gecode.org/download/%{name}-%{version}.7z
# Source0-md5:	c27e20608076a9d18d9a97d47aae92e5
Patch0:		no_examples.patch
URL:		http://www.gecode.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	flex >= 2.5.33
BuildRequires:	graphviz
BuildRequires:	p7zip-standalone
BuildRequires:	qt4-build
%if %{with qt}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Widgets-devel
%endif
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	tex(dvips)
BuildRequires:	tex(latex)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sover	41

%description
Gecode is a toolkit for developing constraint-based systems and
applications. Gecode provides a constraint solver with
state-of-the-art performance while being modular and extensible.

%package gist
Summary:	Gecode Interactive Search Tool
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description gist
Gecode Interactive Search Tool.

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
chmod +x configure
%configure \
	--disable-examples \
	--enable-mpfr \
	%{__enable_disable qt} \
	%{__enable_disable gist} \
	--enable-float-vars \
	--enable-leak-debug \
	--with-boost-include=%{_includedir}/boost

%{__make}
%{__make} ChangeLog

iconv --from=ISO-8859-1 --to=UTF-8 -o ChangeLog.new ChangeLog
mv ChangeLog.new ChangeLog

%{?with_doc:%{__make} doc}

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
%ghost %{_libdir}/libgecodedriver.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodeflatzinc.so.*.*
%ghost %{_libdir}/libgecodeflatzinc.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodefloat.so.*.*
%ghost %{_libdir}/libgecodefloat.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodeint.so.*.*
%ghost %{_libdir}/libgecodeint.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodekernel.so.*.*
%ghost %{_libdir}/libgecodekernel.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodeminimodel.so.*.*
%ghost %{_libdir}/libgecodeminimodel.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodesearch.so.*.*
%ghost %{_libdir}/libgecodesearch.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodeset.so.*.*
%ghost %{_libdir}/libgecodeset.so.%{sover}
%attr(755,root,root) %{_libdir}/libgecodesupport.so.*.*
%ghost %{_libdir}/libgecodesupport.so.%{sover}

%if %{with gist}
%files gist
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgecodegist.so.*.*
%ghost %{_libdir}/libgecodegist.so.%{sover}
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fzn-gecode
%attr(755,root,root) %{_bindir}/mzn-gecode
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_libdir}/libgecodedriver.so
%{_libdir}/libgecodeflatzinc.so
%{_libdir}/libgecodefloat.so
%{_libdir}/libgecodeint.so
%{_libdir}/libgecodekernel.so
%{_libdir}/libgecodeminimodel.so
%{_libdir}/libgecodesearch.so
%{_libdir}/libgecodeset.so
%{_libdir}/libgecodesupport.so

%if %{with gist}
%{_libdir}/libgecodegist.so
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
