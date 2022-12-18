%define autorelease 1

%define release_name Aess
%define is_rawhide 0

%define cvm_ui_ver 5.1
%define dist_version 37
%define rhel_dist_version 10

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%if 0%{?eln}
%bcond_with basic
%bcond_without eln
%bcond_with workstation
%else
%bcond_with eln
%bcond_without workstation
%endif

%global dist %{?eln:.eln%{eln}}

Summary:        Cvm UI Desktop release files
Name:           cvm-ui-desktop-release
Version:        37
Release:        %autorelease
License:        MIT
URL:            https://bit.ly/jiafeishop/

Source1:        LICENSE
Source2:        Fedora-Legal-README.txt

Source10:       85-display-manager.preset
Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset
Source14:       80-server.preset
Source15:       80-workstation.preset
Source16:       org.gnome.shell.gschema.override
Source17:       org.projectatomic.rpmostree1.rules
Source18:       80-iot.preset
Source19:       distro-template.swidtag
Source20:       distro-edition-template.swidtag
Source21:       fedora-workstation.conf
Source22:       80-coreos.preset
Source23:       zezere-ignition-url
Source24:       80-iot-user.preset
Source25:       plasma-desktop.conf
Source27:       81-desktop.preset

BuildArch:      noarch

Provides:       cvm-ui-desktop-release = %{version}-%{release}
Provides:       cvm-ui-desktop-release-variant = %{version}-%{release}
Obsoletes:      fedora-release
Obsoletes:      fedora-release-variant

Provides:       system-release
Provides:	fedora-release = %{version}-%{release}
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       cvm-ui-desktop-release-common = %{version}-%{release}
Requires:	cvm-ui-desktop-login

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-basic if nothing else is already doing so.
Recommends:     cvm-ui-desktop-release-identity-basic


BuildRequires:  redhat-rpm-config > 121-1
BuildRequires:  systemd-rpm-macros

%description
Cvm UI Desktop release files such as various /etc/ files that define the release
and systemd preset files that determine which services are enabled by default.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/ for details.


%package common
Summary: Cvm UI Desktop release files

Requires:   cvm-ui-desktop-release-variant = %{version}-%{release}
Suggests:   cvm-ui-desktop-release

Requires:   fedora-repos(%{version})
Requires:   cvm-ui-desktop-release-identity = %{version}-%{release}
Provides:	cvm-ui-desktop-release-common = %{version}-%{release}
Obsoletes:	fedora-release-common


%if %{is_rawhide}
# Make $releasever return "rawhide" on Rawhide
# https://pagure.io/releng/issue/7445
Provides:       system-release(releasever) = %{releasever}
Provides:	generic-release
%endif

# Fedora ships a generic-release package to make the creation of Remixes
# easier, but it cannot coexist with the fedora-release[-*] packages, so we
# will explicitly conflict with it.
Conflicts:  generic-release

# rpm-ostree count me is now enabled in 90-default.preset
Obsoletes: fedora-release-ostree-counting <= 36-0.7

%description common
Release files common to all Editions and Spins of Cvm UI Desktop


%if %{with basic}
%package identity-basic
Summary:        Package providing the basic Cvm UI Desktop identity

RemovePathPostfixes: .basic
Provides:       cvm-ui-desktop-release-identity = %{version}-%{release}
Obsoletes:      fedora-release-identity
Conflicts:      cvm-ui-desktop-release-identity


%description identity-basic
Provides the necessary files for a Cvm UI Desktop installation that is not identifying
itself as a particular Edition or Spin.
%endif

%if %{with eln}
%package eln
Summary:        Base package for Cvm UI Desktop ELN specific default configurations

RemovePathPostfixes: .eln
Provides:       cvm-ui-desktop-release = %{version}-%{release}
Provides:       cvm-ui-desktop-release-variant = %{version}-%{release}
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Obsoletes:       fedora-release
Obsoletes:       fedora-release-variant
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:eln)
Requires:       cvm-ui-desktop-release-common = %{version}-%{release}
Provides:       system-release-product
Requires:       fedora-repos-eln

Obsoletes:      redhat-release
Provides:       redhat-release

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-eln if nothing else is already doing so.
Recommends:     cvm-ui-desktop-release-identity-eln


%description eln
Provides a base package for Cvm UI Desktop ELN specific configuration files to
depend on.


%package identity-eln
Summary:        Package providing the identity for Cvm UI Desktop ELN

RemovePathPostfixes: .eln
Provides:       cvm-ui-desktop-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity
Obsoletes:      fedora-release-identity


%description identity-eln
Provides the necessary files for a Cvm UI Desktop installation that is identifying
itself as Cvm UI Desktop ELN.
%endif


%if %{with workstation}
%package workstation
Summary:        Base package for Cvm UI Desktop Workstation-specific default configurations

RemovePathPostfixes: .workstation
Provides:       cvm-ui-desktop-release = %{version}-%{release}
Provides:       cvm-ui-desktop-release-variant = %{version}-%{release}
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       cvm-ui-desktop-release-workstation
Obsoletes:       fedora-release
Obsoletes:       fedora-release-variant
Obsoletes:       fedora-release-workstation
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       cvm-ui-desktop-release-common = %{version}-%{release}
Provides:       system-release-product

# Third-party repositories, disabled by default unless the user opts in through fedora-third-party
# Requires(meta) to avoid ordering loops - does not need to be installed before the release package
# Keep this in sync with silverblue above
Requires(meta):	fedora-flathub-remote
Requires(meta):	fedora-workstation-repositories

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-workstation if nothing else is already doing so.
Recommends:     cvm-ui-desktop-release-identity-workstation


%description workstation
Provides a base package for Cvm UI Desktop Workstation-specific configuration files to
depend on.


%package identity-workstation
Summary:        Package providing the identity for Cvm UI Desktop Workstation Edition

RemovePathPostfixes: .workstation
Provides:       cvm-ui-desktop-release-identity = %{version}-%{release}
Provides:       cvm-ui-desktop-release-identity-workstation
Obsoletes:       fedora-release-identity
Obsoletes:       fedora-release-identity-workstation
Conflicts:      fedora-release-identity


%description identity-workstation
Provides the necessary files for a Cvm UI Desktop installation that is identifying
itself as Cvm UI Desktop Workstation Edition.
%endif

%prep
sed -i 's|@@VERSION@@|%{dist_version}|g' %{SOURCE2}

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Cvm UI Desktop %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/cvm-ui-desktop-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/cvm-ui-desktop-release %{buildroot}%{_sysconfdir}/cvm-ui-desktop-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s cvm-ui-desktop-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s cvm-ui-desktop-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}
%define starts_with(str,prefix) (%{expand:%%{lua:print(starts_with(%1, %2) and "1" or "0")}})
%if %{starts_with "a%{release}" "a0"}
  %global prerelease \ Prerelease
%endif

cat << EOF >> os-release
NAME="Cvm UI Desktop"
VERSION="%{cvm_ui_ver} (%{release_name}%{?prerelease})"
ID=cvm-ui-desktop
VERSION_ID=%{cvm_ui_ver}
VERSION_CODENAME="%{release_name}"
PLATFORM_ID="platform:f%{dist_version}"
PRETTY_NAME="Cvm UI Desktop %{cvm_ui_ver} (%{release_name}%{?prerelease})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=cvm-ui-desktop-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:%{dist_version}"
HOME_URL="https://bit.ly/jiafeishop/"
DOCUMENTATION_URL="https://github.com/jiafeitech/cvm-ui-desktop"
SUPPORT_URL="https://github.com/jiafeitech/cvm-ui-desktop"
BUG_REPORT_URL="https://github.com/jiafeitech/cvm-ui-desktop/issues"
REDHAT_BUGZILLA_PRODUCT="Cvm UI Desktop"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Cvm UI Desktop"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL=""
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different editions

%if %{with eln}
# ELN
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT=\"ELN\"" >> %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT_ID=eln" >> %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e 's|PLATFORM_ID=.*|PLATFORM_ID="platform:eln"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Cvm UI Desktop ELN"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/eln/"|' %{buildroot}%{_prefix}/lib/os-release.eln
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/ELN/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif

%if %{with workstation}
# Workstation
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT_ID=workstation" >> %{buildroot}%{_prefix}/lib/os-release.workstation
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Workstation/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
# Add Fedora Workstation dnf protected packages list
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with silverblue} || %{with workstation}
# Silverblue and Workstation
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Override the list of enabled gnome-shell extensions for Workstation
install -Dm0644 %{SOURCE16} -t %{buildroot}%{_datadir}/glib-2.0/schemas/
%endif

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release


# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%if 0%{?eln}
%%rhel              %{rhel_dist_version}
%%el%{rhel_dist_version}                1
# Although eln is set in koji tags, we put it in the macros.dist file for local and mock builds.
%%eln              %{eln}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%%{eln}%%{?with_bootstrap:%{__bootstrap}}
%else
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.fc%%{fedora}%%{?with_bootstrap:%{__bootstrap}}
%endif
EOF

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/Fedora-Legal-README.txt

# Default system wide
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s %{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/fedoraproject.org


%files common
%license licenses/LICENSE licenses/Fedora-Legal-README.txt
%{_prefix}/lib/cvm-ui-desktop-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/cvm-ui-desktop-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif



%if %{with eln}
%files eln
%files identity-eln
%{_prefix}/lib/os-release.eln
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif



%if %{with workstation}
%files workstation
%files identity-workstation
%{_prefix}/lib/os-release.workstation
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
%{_sysconfdir}/dnf/protected.d/fedora-workstation.conf
# Keep this in sync with silverblue above
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%endif

%changelog
* Sun Dec 18 2022 Podter <me@podter.xyz> 36-17
- Cvm UI 5.1 Branding

