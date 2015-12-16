%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

%global gem_name i18n

Summary: New wave Internationalization support for Ruby
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.6.11
Release: 1%{?dist}
Group: Development/Languages
License: MIT and (BSD or Ruby)
URL: http://github.com/svenfuchs/i18n
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(test_declarative)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Ruby Internationalization and localization solution.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires:%{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
# skipping check section, it fails with:
#[deprecated] I18n.enforce_available_locales will default to true in the future. If you really want to skip validation of your locale you can set I18n.enforce_available_locales = false to avoid this message.
#[DEPRECATED] I18n's :recue_format option will be removed from a future release. All exception messages will be plain text. If you need the exception handler to return an html format please set or pass a custom exception handler.
exit 0

pushd .%{gem_instdir}

# Bundler just complicates everything in our case, remove it.
sed -i -e "s|require 'bundler/setup'||" test/test_helper.rb
# Tests are failing without LANG environment is set.
# https://github.com/svenfuchs/i18n/issues/115
# 2 errors on Ruby 2.2
# https://github.com/svenfuchs/i18n/commit/2b48cb36cdcc881dadfa20b1b4f670c02af9a5c4
%{?scl:scl enable %scl - << \EOF}
LANG=en_US.utf8 ruby -Ilib:test -rset -e 'require "./test/all.rb"' | grep '.*0 failures, 2 errors.*'
%{?scl:EOF}

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/MIT-LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/test
%{gem_instdir}/gemfiles
%doc %{gem_docdir}


%changelog
* Fri Jan 16 2015 Josef Stribny <jstribny@redhat.com> - 0.6.11-1
- Update to 0.6.11

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.4-3
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Tue Feb 04 2014 Josef Stribny <jstribny@redhat.com> - 0.6.4-2
- Fix license: Ruby is now licensed under BSD or Ruby

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 0.6.4-1
- Update to i18n 

* Fri Jun 07 2013 Josef Stribny <jstribny@redhat.com> - 0.6.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to i18n 0.6.1

* Tue Jul 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-3
- Exclude the cached gem.

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-2
- Specfile cleanup

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-1
- Rebuilt for scl.
- Updated to 0.6.0.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.0-3
- Rebuilt for Ruby 1.9.3.
- Enabled test suite.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 Vít Ondruch <vondruch@redhat.com> - 0.5.0-1
- Update to i18n 0.5.0.
- Documentation moved into subpackage.
- Removed unnecessary cleanup.
- Preparetion for test suite execution during build.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-2
- Add GPLv2 or Ruby License
- Files MIT-LICENSE, geminstdir/lib/i18n.rb are non executable now

* Thu Nov 11 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-1
- Initial package
