# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/NX/bin/nxserver.bin; \

%define selinux_policyver 3.12.1-69

Name:   nx-server_selinux
Version:	1.0
Release:	2%{?dist}
Summary:	SELinux policy module for nx-server

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	nx-server.pp
Source1:	nx-server.if
Source2:	nx-server_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for nx-server.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/nx-server_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/nx-server.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r nx-server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/nx-server.pp
%{_datadir}/selinux/devel/include/contrib/nx-server.if
%{_mandir}/man8/nx-server_selinux.8.*


%changelog
* Sun Aug 25 2013 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

