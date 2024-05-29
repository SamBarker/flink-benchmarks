#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
import argparse, subprocess, shlex

DEFAULT_BENCHMARK_PATTERN = ".*"

parser = argparse.ArgumentParser(description='Execute a set of JMH benchmarks')

parser.add_argument('--jvm-args', dest='jvm_args', required=False, type=str, action="store",
                    help='an argument to pass to the JVM executing the benchmark suite')
parser.add_argument('--classpath', dest='classpath', required=False, type=str,
                    help='The class path to run the benchmark suite.')
parser.add_argument('--jvm', dest='executable', required=False, default="java", type=str,
                    help='The path to  the java executable to run the benchmark suite.')
parser.add_argument('--jmh-args', dest='jmh_args', required=False, type=str, action="append",
                    help="passes arguments to control JMH execution")
parser.add_argument('--profiler', dest='profiler_arg', required=False, type=str,
                    help="The JMH -prof string to configure the profiler")
parser.add_argument('--benchmark-excludes', dest='benchmark_exclusions', required=False, type=str,
                    help="A regular expression used by JMH to exclude benchmarks from the benchmark run")
parser.add_argument('benchmarks', default=DEFAULT_BENCHMARK_PATTERN,
                    help='A regular expression used by JMH to select the benchmarks to run, default: %s'
                         % DEFAULT_BENCHMARK_PATTERN)

args = parser.parse_args()
__command_args = [args.executable]
__command_args += shlex.split(args.jvm_args.replace("'", ""))
__command_args.append("-cp")
__command_args.append(args.classpath)
__command_args.append("org.openjdk.jmh.Main")
__command_args += shlex.split("-foe true -rf csv")
__command_args += args.jmh_args or ""

if args.benchmark_exclusions:
    __command_args.append("-e")
    __command_args.append(args.benchmark_exclusions)
if args.profiler_arg:
    __command_args.append("-prof")
    __command_args.append(args.profiler_arg)

__command_args.append(args.benchmarks)

__command_args = [arg for arg in __command_args if arg is not None and arg != ""]

print("Executing: %s" % __command_args)
run = subprocess.run(__command_args, check=False, capture_output=False, encoding="utf-8", shell=False)
