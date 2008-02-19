#TODO
#- udev rules
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel
%bcond_with	verbose		# verbose build (V=1)
#
%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		rel	16
Summary:	Toshiba Laptop Bluetooth module
Summary(pl.UTF-8):	Moduł Bluetooth dla laptopów Toshiby
Name:		toshbt
Version:	1.0
Release:	%{rel}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://0bits.com/toshbt/%{name}-%{version}.tar.gz
# Source0-md5:	8e4764f6c438427b00fb9aa93abb3cd7
URL:		http://0bits.com/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Toshiba Laptop Bluetooth module.

%description -l pl.UTF-8
Moduł Bluetooth dla laptopów Toshiby.

%package -n kernel%{_alt_kernel}-misc-%{name}
Summary:	Linux driver for Toshiba Laptop Bluetooth
Summary(pl.UTF-8):	Sterownik dla Linuksa dla Bluetooth w Laptopach Toshiba
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires:	module-init-tools >= 3.2.2-2
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-misc-%{name}
This is driver for Bluetooth in Toshiba Laptops for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-misc-%{name} -l pl.UTF-8
Sterownik dla Linuksa dla Bluetooth w Laptopach Toshiba.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{name}

%build
%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{name} -d misc -n %{name} -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-misc-%{name}
%defattr(644,root,root,755)
/etc/modprobe.d/%{_kernel_ver}/%{name}.conf
/lib/modules/%{_kernel_ver}/misc/%{name}-current.ko*
