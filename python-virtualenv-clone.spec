#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	virtualenv-clone
Summary:	Script to clone virtualenvs
Name:		python-virtualenv-clone
Version:	0.2.4
Release:	4
License:	MIT
Group:		Development/Libraries
Source0:	http://pypi.python.org/packages/source/v/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	71168b975eaaa91e65559bcc79290b3b
URL:		http://pypi.python.org/pypi/virtualenv-clone
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	python-virtualenv
%endif
%if %{with python3}
BuildRequires:	python3-virtualenv
%endif
Requires:	python-virtualenv
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A script for cloning a non-relocatable virtualenv.

Virtualenv provides a way to make virtualenv's relocatable which could
then be copied as we wanted. However making a virtualenv relocatable
this way breaks the no-site-packages isolation of the virtualenv as
well as other aspects that come with relative paths and '/usr/bin/env'
shebangs that may be undesirable.

Also, the .pth and .egg-link rewriting doesn't seem to work as
intended. This attempts to overcome these issues and provide a way to
easily clone an existing virtualenv.

%package -n python3-virtualenv-clone
Summary:	Script to clone virtualenvs
Group:		Development/Libraries
Requires:	python3-virtualenv

%description -n python3-virtualenv-clone
virtualenv cloning script.

A script for cloning a non-relocatable virtualenv.

Virtualenv provides a way to make virtualenv's relocatable which could
then be copied as we wanted. However making a virtualenv relocatable
this way breaks the no-site-packages isolation of the virtualenv as
well as other aspects that come with relative paths and '/usr/bin/env'
shebangs that may be undesirable.

Also, the .pth and .egg-link rewriting doesn't seem to work as
intended. This attempts to overcome these issues and provide a way to
easily clone an existing virtualenv.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/virtualenv-clone
%{py_sitescriptdir}/clonevirtualenv.py[co]
%{py_sitescriptdir}/virtualenv_clone-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/virtualenv-clone
%{py3_sitescriptdir}/clonevirtualenv.*
%{py3_sitescriptdir}/virtualenv_clone-%{version}-*
%{py3_sitescriptdir}/__pycache__/*clonevirtualenv*
%endif
