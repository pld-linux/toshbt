#TODO
#- spec filename vs Name
#- udev rules
#- modprobe.d
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	Toshiba Laptop Bluetooth module
Summary(pl):	Modu³ Bluetooth dla laptopów Toshiby
Name:		toshbt
Version:	1.0
Release:	%{_rel}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://0bits.com/toshbt/%{name}-%{version}.tar.gz
# Source0-md5:	8e4764f6c438427b00fb9aa93abb3cd7
URL:		http://0bits.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.308
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Toshiba Laptop Bluetooth module.

%description -l pl
Modu³ Bluetooth dla laptopów Toshiby.

%package -n kernel%{_alt_kernel}-misc-%{name}
Summary:	Linux driver for Toshiba Laptop Bluetooth
Summary(pl):	Sterownik dla Linuksa dla Bluetooth w Laptopach Toshiba
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-misc-%{name}
This is driver for Bluetooth in Toshiba Laptops for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-misc-%{name} -l pl
Sterownik dla Linuksa dla Bluetooth w Laptopach Toshiba.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-misc-%{name}
Summary:	Linux SMP driver for Toshiba Laptop Bluetooth.
Summary(pl):	Sterownik dla Linuksa SMP  Bluetooth w Laptopach Toshiba.
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-misc-%{name}
This is driver for Bluetooth in Toshiba Laptops for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-misc-%{name} -l pl
Sterownik dla Linuksa dla Bluetooth w Laptopach Toshiba.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{name}

%build

%if %{with kernel}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv %{name}{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install %{name}-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{name}.ko
%if %{with smp} && %{with dist_kernel}
install %{name}-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{name}.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
%endif
