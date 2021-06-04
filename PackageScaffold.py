import os
import shutil

class PackageScaffold():
    """Create boilerplate for a python CLI app package.
    TODO: Convert to package, upload to github.
    TODO: Interactive prompt form setup fields.
    TODO: Rename package.
    TODO: Change description.
    TODO: Update package version.
    """

    def __init__(self, vpkg_name, vpkg_desc, vpkg_path):
        """Define all package metadata."""
        self.vpkg_name = vpkg_name
        self.vpkg_desc = vpkg_desc

        self.vpkg_author = "Daniel Velez"
        self.vpkg_email = "daniel.enr.velez@gmail.com"
        self.vpkg_git_account = "AnikaSystems"
        self.vpkg_py_version = "3.6"
        self.vpkg_license = "Copyright Anikasystems"
        
        # Pacakage paths.
        self.vpkg_path = os.path.abspath(vpkg_path)
        self.vpkg_source = os.path.join(vpkg_path, vpkg_name)
        self.vpkg_subsource = os.path.join(self.vpkg_source, vpkg_name)

    ## String manipulation #####################################################

    def trim_lines(self, vstring):
        """Trim all the trailing spaces in each line of string."""
        vlines = vstring.split('\n')
        vres = ""
        for vline in vlines: vres += vline.strip()+"\n"
        return vres.strip()

    def underscore_to_camelcase(self, vstring):
        """Convert a name sperated with underscores into camelcase."""
        vwords = vstring.split("_")
        vres = ""
        for vword in vwords: vres += vword.capitalize()
        return vres

    def break_string (self, vstring, vsize):
        """Break a string into lines of `vsize` length."""
        vres = ""
        vstring = vstring.strip().replace('\n', ' ')
        vwords = vstring.split(' ')
        vcurlen = 0
        for vword in vwords:
            vword = vword.strip()
            if vcurlen + len(vword) >= vsize:
                vres += '\n'
                vcurlen = 0
            vres += vword + ' '
            vcurlen += len(vword)+1
        return vres
        
    ## Scaffolding functions ###################################################

    def create_readme(self):
        vprog_name = self.vpkg_name.replace("_", "-")
        vreadme = self.trim_lines(f"""
        # {self.vpkg_name} #
        {self.break_string(self.vpkg_desc, 80)}


        ## installation ##
        Requires `Python >= {self.vpkg_py_version}`. 
        Use `pip` to install directly from github:
        ```bash
        $ python -m pip install git+https://github.com/{self.vpkg_git_account}/{self.vpkg_name}.git 
        ```
        This will expose the command `{vprog_name}.exe`. See below for usage.

        ### from source ###
        To install from source, simply `clone` the repo, `cd` into it, and run the 
        `setup.py` install script.
        ```bash
        $ git clone https://github.com/{self.vpkg_git_account}/{self.vpkg_name}.git
        $ cd {self.vpkg_name}
        $ python setup.py install
        ```


        ## usage ##
        ```bash
        ```


        ## running locally ##
        To test the module locally without installing, `cd` into the project 
        root and type `python -m {self.vpkg_name}`. This will run the modules 
        entry point, which happens to be a CLI.
        """)
        
        vreadme_path = os.path.join(self.vpkg_source, "README.md")
        open(vreadme_path, "w+").write(vreadme)
        

    def create_gitignore(self):
        vgitignore = self.trim_lines("""
        *.swp
        .*.swp
        __pycache__/
        dist/
        *.egg-info/
        eggs/
        .eggs/
        build/
        """)
        vignore_path = os.path.join(self.vpkg_source, ".gitignore")
        open(vignore_path, "w+").write(vgitignore)

    def create_setup(self):
        """Create setup file with CLI entry point."""
        vprog_name = self.vpkg_name.replace("_", "-") 
        vsetup_string = self.trim_lines(f"""
        #!/usr/bin/python
        from setuptools import setup, find_packages

        setup(name='{self.vpkg_name}',
            version='0.0.1',
            description='{self.vpkg_desc}',
            url='https://github.com/{self.vpkg_git_account}/{self.vpkg_name}',
            author='{self.vpkg_author}',
            author_email='{self.vpkg_email}',
            license='{self.vpkg_license}',
            python_requires=">={self.vpkg_py_version}",
            packages=['{self.vpkg_name}'],
            entry_points = {{
                'console_scripts': [
                    '{vprog_name}={self.vpkg_name}.__main__:main'
                ]
            }},
            install_requires=[])
        """)
        vsetup_path = os.path.join(self.vpkg_source, "setup.py")
        open(vsetup_path, "w+").write(vsetup_string)

    def create_source_folder(self):
        """Creates the __init__.py, __main__.py, and main class files."""
        vinit_path = os.path.join(self.vpkg_subsource, "__init__.py")
        open(vinit_path, "w+").write("")
        
        # Create __main__ entry point.
        vmain_path = os.path.join(self.vpkg_subsource, "__main__.py")
        vclass_name = self.underscore_to_camelcase(self.vpkg_name)
        vmain_text = self.trim_lines(f"""
        \"\"\"{self.break_string(self.vpkg_desc, 80)}\"\"\""
        #!/usr/bin/python
        import sys
        import argparse

        from {self.vpkg_name}.{vclass_name} import {vclass_name}


        def main():
            \"\"\"Run CLI for {self.vpkg_name.replace("_", "-")}.\"\"\"
            parser = argparse.ArgumentParser(
                prog="{self.vpkg_name.replace("_", "-")}",
                description="{self.vpkg_desc}"
            )

            args = parser.parse_args()


        if __name__ == "__main__":
            # Use this entry point to test the package locally.
            main()
        """)
        open(vmain_path, "w+").write(vmain_text)
        
        # Create main class.
        vclass_path = os.path.join(self.vpkg_subsource, vclass_name+".py")
        vclass_text = self.trim_lines(f"""
        class {vclass_name}:
            \"\"\"Enter class description.\"\"\"
            pass
        """)
        open(vclass_path, "w+").write(vclass_text)

    ## Command functions ####################################################### 

    def clean(self):
        """Removes the package directory to reinstatiate it later."""
        vpkg_path = os.path.join(self.vpkg_path, self.vpkg_name)
        try:
            shutil.rmtree(vpkg_path)
        except Exception as e:
            print("[* scaffold] Error: cannot clean. Path %s nonexistent." 
                % vpkg_path)
            # print(e)
            return

    def update_package_version(self):
        """Updates the package version within the setup.py"""
        return

    def scaffold_prompt(self):
        """Run interactive prompt to get package details from user."""
        return

    def scaffold(self):
        """Run entire scffolding process"""
        # Create initial directory.
        vpkg_path = os.path.join(self.vpkg_path, self.vpkg_name)
        try:
            os.mkdir(vpkg_path)
        except FileExistsError as e:
            print("[* scaffold] Error: path %s already exists." % vpkg_path)
            return

        # Create subdirectory for source code.
        os.mkdir(os.path.join(vpkg_path, self.vpkg_name))

        # Initialize as git repo.
        os.chdir(vpkg_path)
        os.system("git init")

        # Run scaffolding subtasks.
        self.create_readme()
        self.create_gitignore()
        self.create_setup()
        self.create_source_folder()


if __name__ == "__main__":
    # Test out scaffold class.
    import os
    scaffold = PackageScaffold(
        vpkg_name="test_package", 
        vpkg_desc="This is a test package!", 
        vpkg_path=os.environ['HOME'])
    scaffold.clean()
    scaffold.scaffold()

    # Scaffold tool for python packages that provide a user CLI.
    # package-scaffold run