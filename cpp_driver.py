# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from os import path, listdir, walk
from subprocess import call
import sys
from PyInquirer import prompt, Separator
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

'''
Driver for Udacity C++ course. This file allows for easily compile & run for cpp and object files.
'''

def walk_directory(ending):
  target_files = []
  mypath = path.dirname(path.realpath(__file__))
  for (dirpath, dinames, filenames) in walk(mypath):
    target_files = filenames
    break;
  return filter(lambda f: f.endswith(ending), target_files)

def print_file_with_style(filename):
  file_ending_tokens = {
    'cpp': Token.Cpp,
    'o': Token.Object
  }
  file_ending = filename.split('.')[1]
  print_tokens([(file_ending_tokens.get(file_ending, Token.Default), ' - ' + filename + '\n')], style=style)


### ------------------------------ Commands ------------------------------ ###
# Command == 'list'
# List all files in the current directory
def list_command():
  print("Listing all files in the current directory:")
  target_files = walk_directory('')
  for file in target_files:
    print_file_with_style(file)

# Command == 'compile'
# Compile a custom cpp source file
def compile_command():
  print("Compile a custom cpp source file:")
  target_files = walk_directory('.cpp')
  target_files.append('none')
  choose_file['choices'] = target_files
  file = prompt(choose_file)
  filename = file['choose_file']
  print(filename)

  if filename == 'none':
    return
  else:
    print("Compiling file: %s" % filename)
    call(['g++', filename, '-o', filename.split('.')[0] + '.o'])

# Command == 'run'
# Run a generated object file
def run_command():
  print("Run a generated object file:")
  target_files = walk_directory('.o')
  target_files.append('none')
  choose_file['choices'] = target_files
  file = prompt(choose_file)
  filename = file['choose_file']
  print(filename)

  if filename == 'none':
    return
  else:
    print("Running file: %s" % filename)
    print("Standard output:\n\n--------")
    call(['./' + filename])
    print("--------\n")

# Command == 'cleanup'
# Deletes all generated object files
def cleanup_command():
  print("Delete all object files in the current directory:")
  target_files = walk_directory('.o')
  for file in target_files:
    print_file_with_style(file)

  confirm = prompt(confirm_delete)
  if confirm['confirm_delete'] == 'Yes':
    for file in target_files:
      call(['rm', file])
  else:
    return

### ---------------------------------------------------------------------- ###

# Switcher function
def execute_command(command):
  switch_command = {
    'list': list_command,
    'compile': compile_command,
    'run': run_command,
    'cleanup': cleanup_command,
    'exit': sys.exit
  }
  switch_command[command]()

def main():
  while(True):
    command = prompt(choose_command)
    execute_command(command['choose_command'])

### ------------------------- PyInquirer prompts ------------------------- ###
choose_command = {
  'type': 'expand',
  'name': 'choose_command',
  'message': 'Enter a command:',
  'default': 'h',
  'choices': [
    {
      'key': 'l',
      'name': 'List the contents of the directory',
      'value': 'list'
    },
    {
      'key': 'c',
      'name': 'Compile a cpp source file',
      'value': 'compile'
    },
    {
      'key': 'r',
      'name': 'Run a generated object file',
      'value': 'run'
    },
    {
      'key': 'd',
      'name': 'Delete all executable object files',
      'value': 'cleanup'
    },
    Separator(),
    {
      'key': 'x',
      'name': 'Exit',
      'value': 'exit'
    }
  ]
}

choose_file = {
  'type': 'rawlist',
  'name': 'choose_file',
  'message': 'Choose a file to operate on:',
  'choices': []
}

confirm_delete = {
  'type': 'rawlist',
  'name': 'confirm_delete',
  'message': 'Are you sure you want to delete these files?',
  'choices': [
    'No',
    'Yes'
  ]
}
### ---------------------------------------------------------------------- ###

### --------------------------- Printer styles --------------------------- ###
style = style_from_dict({
  Token.Cpp: '#00acc1',
  Token.Object: '#e53935',
  Token.Default: '#FFFFFF'
})
### ---------------------------------------------------------------------- ###

if __name__ == '__main__':
  main()
