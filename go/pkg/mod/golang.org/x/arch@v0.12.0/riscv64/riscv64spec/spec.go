// Copyright 2024 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// riscv64spec reads the files contained in riscv-opcodes repo
// to collect instruction encoding details.
// repo url: https://github.com/riscv/riscv-opcodes
// usage: go run spec.go <opcodes-repo-path>

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

// RV64GC_zba_zbb_zbs Extensions Listing
// Reference: $GOROOT/src/src/cmd/internal/obj/riscv/inst.go
var extensions = []string{
	"rv_a",
	"rv_c",
	"rv_c_d",
	"rv_d",
	"rv_f",
	"rv_i",
	"rv_m",
	"rv_q",
	"rv_zba",
	"rv_zbb",
	"rv_zbs",
	"rv_zfh",
	"rv_zicsr",
	"rv_zifencei",
	"rv64_a",
	"rv64_c",
	"rv64_d",
	"rv64_f",
	"rv64_i",
	"rv64_m",
	"rv64_q",
	"rv64_zba",
	"rv64_zbb",
	"rv64_zbs",
	"rv64_zfh",
}

const (
	prologueSec    = "// Code generated by riscv64spec riscv-opcodes\n// DO NOT EDIT\n\n// Copyright 2024 The Go Authors. All rights reserved.\n// Use of this source code is governed by a BSD-style\n// license that can be found in the LICENSE file.\n\npackage riscv64asm\n\n"
	opSec          = "const (\n\t_ Op = iota\n"
	opstrSec       = "var opstr = [...]string{\n"
	instFormatsSec = "var instFormats = [...]instFormat{\n"
)

var (
	ops                []string
	opstrs             = make(map[string]string)
	instFormatComments = make(map[string]string)
	instFormats        = make(map[string]string)
)

func main() {
	log.SetFlags(0)
	log.SetPrefix("riscv64spec: ")

	var repoPath string
	if len(os.Args) < 1 {
		log.Fatal("usage: go run spec.go <opcodes-repo-path>")
	}
	repoPath = os.Args[1]

	fileTables, err := os.Create("tables.go")
	if err != nil {
		log.Fatal(err)
	}

	buf := bufio.NewWriter(fileTables)
	_, err = buf.Write([]byte(prologueSec))
	if err != nil {
		log.Fatal(err)
	}

	for _, ext := range extensions {
		f, err := os.Open(filepath.Join(repoPath, ext))
		if err != nil {
			log.Fatal(err)
		}
		defer f.Close()

		buf := bufio.NewScanner(f)
		for buf.Scan() {
			line := buf.Text()
			if len(line) == 0 {
				continue
			}
			words := strings.Fields(line)
			if len(words) == 0 || words[0][0] == '#' {
				continue
			}

			// skip $pseudo_op except rv_zbb/rv64_zbb
			if words[0][0] == '$' {
				if ext != "rv_zbb" && ext != "rv64_zbb" {
					continue
				}
				words = words[2:]
			}

			genInst(words)
		}
	}

	// c.unimp wasn't in riscv-opcodes, so add it there
	c_unimp := "c.unimp 15..0=0"
	genInst(strings.Fields(c_unimp))

	sort.Strings(ops)

	// 1. write op
	if _, err := buf.Write([]byte(opSec)); err != nil {
		log.Fatal(err)
	}
	for _, op := range ops {
		if _, err := fmt.Fprintf(buf, "\t%s\n", op); err != nil {
			log.Fatal(err)
		}
	}
	if _, err := buf.Write([]byte(")\n\n")); err != nil {
		log.Fatal(err)
	}

	// 2. write opstr
	if _, err := buf.Write([]byte(opstrSec)); err != nil {
		log.Fatal(err)
	}
	for _, op := range ops {
		if _, err := fmt.Fprintf(buf, "\t%s\n", opstrs[op]); err != nil {
			log.Fatal(err)
		}
	}
	if _, err := buf.Write([]byte("}\n\n")); err != nil {
		log.Fatal(err)
	}

	// 3. write instFormatComment and instFormat
	if _, err := buf.Write([]byte(instFormatsSec)); err != nil {
		log.Fatal(err)
	}
	for _, op := range ops {
		if _, err := fmt.Fprintf(buf, "\t%s\n\t%s\n", instFormatComments[op], instFormats[op]); err != nil {
			log.Fatal(err)
		}
	}
	if _, err = buf.Write([]byte("}\n")); err != nil {
		log.Fatal(err)
	}

	if err := buf.Flush(); err != nil {
		log.Fatal(err)
	}

	if err := fileTables.Close(); err != nil {
		log.Fatal(err)
	}
}

func genInst(words []string) {
	op := strings.ToUpper(strings.Replace(words[0], ".", "_", -1))
	opstr := fmt.Sprintf("%s:\t\"%s\",", op, strings.ToUpper(words[0]))

	var value uint32
	var mask uint32
	var argTypeList []string

	for i := 1; i < len(words); i++ {
		if strings.Contains(words[i], "=") {
			val := strings.Split(words[i], "=")
			sec := strings.Split(val[0], "..")
			if len(sec) < 2 {
				sec[0] = val[0]
			}
			subval, submsk := genValueAndMask(val, sec)
			value |= subval
			mask |= submsk
		} else if len(words[i]) > 0 {
			argTypeList = append(argTypeList, words[i])
		}
	}

	instArgsStr := inferFormats(argTypeList, op)
	instFormatComment := "// " + strings.Replace(op, "_", ".", -1) + " " + strings.Replace(instArgsStr, "arg_", "", -1)
	instFormat := fmt.Sprintf("{mask: %#08x, value: %#08x, op: %s, args: argTypeList{%s}},", mask, value, op, instArgsStr)

	// Handle the suffix of atomic instruction.
	if isAtomic(op) {
		suffix := []string{"", ".RL", ".AQ", ".AQRL"}
		// Re-generate the opcode string, opcode value and mask.
		for i, suf := range suffix {
			aop := op + strings.Replace(suf, ".", "_", -1)
			aopstr := fmt.Sprintf("%s:\t\"%s\",", aop, strings.ToUpper(words[0])+suf)
			avalue := value | (uint32(i) << 25)
			amask := mask | 0x06000000
			ainstFormatComment := "// " + strings.Replace(aop, "_", ".", -1) + " " + strings.Replace(instArgsStr, "arg_", "", -1)
			ainstFormat := fmt.Sprintf("{mask: %#08x, value: %#08x, op: %s, args: argTypeList{%s}},", amask, avalue, aop, instArgsStr)
			ops = append(ops, aop)
			opstrs[aop] = aopstr
			instFormats[aop] = ainstFormat
			instFormatComments[aop] = ainstFormatComment
		}
	} else {
		ops = append(ops, op)
		opstrs[op] = opstr
		instFormats[op] = instFormat
		instFormatComments[op] = instFormatComment
	}
}

// inferFormats identifies inst format:
// R-Type (inst rd, rs1, rs2),
// I-Type (inst rd, rs1, imm / inst rd, offset(rs1)),
// UJ-Type (inst rd, imm),
// U-Type (inst rd, imm),
// SB-Type (inst rs1, rs2, offset)
// S-Type (inst rs2, offset(rs1))
func inferFormats(argTypeList []string, op string) string {
	switch {
	case strings.Contains(op, "AMO") || strings.Contains(op, "SC_"):
		return "arg_rd, arg_rs2, arg_rs1_amo"

	case strings.Contains(op, "LR_"):
		return "arg_rd, arg_rs1_amo"

	case op == "LB" || op == "LBU" || op == "LD" ||
		op == "LH" || op == "LHU" || op == "LW" || op == "LWU":
		return "arg_rd, arg_rs1_mem"

	case op == "FLD" || op == "FLW" || op == "FLH" || op == "FLQ":
		return "arg_fd, arg_rs1_mem"

	case op == "FSD" || op == "FSW" || op == "FSH" || op == "FSQ":
		return "arg_fs2, arg_rs1_store"

	case op == "SD" || op == "SB" || op == "SW" || op == "SH":
		return "arg_rs2, arg_rs1_store"

	case op == "CSRRW" || op == "CSRRS" || op == "CSRRC":
		return "arg_rd, arg_csr, arg_rs1"

	case op == "CSRRWI" || op == "CSRRSI" || op == "CSRRCI":
		return "arg_rd, arg_csr, arg_zimm"

	case op == "JALR":
		return "arg_rd, arg_rs1_mem"

	case op == "FENCE_I":
		return ""

	case op == "FENCE":
		return "arg_pred, arg_succ"

	default:
		var instStr []string
		for _, arg := range argTypeList {
			if decodeArgs(arg, op) != "" {
				instStr = append(instStr, decodeArgs(arg, op))
			}
		}
		return strings.Join(instStr, ", ")
	}
}

// decodeArgs turns the args into formats defined in arg.go
func decodeArgs(arg string, op string) string {
	switch {
	case strings.Contains("arg_rd", arg):
		if isFloatReg(op, "rd") || strings.Contains(op, "C_FLDSP") {
			return "arg_fd"
		}
		return "arg_rd"

	case strings.Contains("arg_rs1", arg):
		if isFloatReg(op, "rs") {
			return "arg_fs1"
		}
		return "arg_rs1"

	case strings.Contains("arg_rs2", arg):
		if isFloatReg(op, "rs") {
			return "arg_fs2"
		}
		return "arg_rs2"

	case strings.Contains("arg_rs3", arg):
		if isFloatReg(op, "rs") {
			return "arg_fs3"
		}
		return "arg_rs3"

	case arg == "imm12":
		return "arg_imm12"

	case arg == "imm20":
		return "arg_imm20"

	case arg == "jimm20":
		return "arg_jimm20"

	case arg == "bimm12lo":
		return "arg_bimm12"

	case arg == "imm12lo":
		return "arg_simm12"

	case arg == "shamtw":
		return "arg_shamt5"

	case arg == "shamtd":
		return "arg_shamt6"

	case arg == "rd_p":
		if strings.Contains(op, "C_FLD") {
			return "arg_fd_p"
		}
		return "arg_rd_p"

	case arg == "rs1_p":
		return "arg_rs1_p"

	case arg == "rd_rs1_p":
		return "arg_rd_rs1_p"

	case arg == "rs2_p":
		if strings.Contains(op, "C_FSD") {
			return "arg_fs2_p"
		}
		return "arg_rs2_p"

	case arg == "rd_n0":
		return "arg_rd_n0"

	case arg == "rs1_n0":
		return "arg_rs1_n0"

	case arg == "rd_rs1_n0":
		return "arg_rd_rs1_n0"

	case arg == "c_rs1_n0":
		return "arg_c_rs1_n0"

	case arg == "c_rs2_n0":
		return "arg_c_rs2_n0"

	case arg == "c_rs2":
		if strings.Contains(op, "C_FSDSP") {
			return "arg_c_fs2"
		}
		return "arg_c_rs2"

	case arg == "rd_n2":
		return "arg_rd_n2"

	case arg == "c_imm6lo":
		return "arg_c_imm6"

	case arg == "c_nzimm6lo":
		return "arg_c_nzimm6"

	case arg == "c_nzuimm6lo":
		return "arg_c_nzuimm6"

	case arg == "c_uimm7lo":
		return "arg_c_uimm7"

	case arg == "c_uimm8lo":
		return "arg_c_uimm8"

	case arg == "c_uimm8sp_s":
		return "arg_c_uimm8sp_s"

	case arg == "c_uimm8splo":
		return "arg_c_uimm8sp"

	case arg == "c_uimm9sp_s":
		return "arg_c_uimm9sp_s"

	case arg == "c_uimm9splo":
		return "arg_c_uimm9sp"

	case arg == "c_bimm9lo":
		return "arg_c_bimm9"

	case arg == "c_nzimm10lo":
		return "arg_c_nzimm10"

	case arg == "c_nzuimm10":
		return "arg_c_nzuimm10"

	case arg == "c_imm12":
		return "arg_c_imm12"

	case arg == "c_nzimm18lo":
		return "arg_c_nzimm18"
	}
	return ""
}

// genValueAndMask generates instruction value and relative mask.
func genValueAndMask(valStr []string, secStr []string) (uint32, uint32) {
	var val int64

	val, err := strconv.ParseInt(valStr[1], 0, 32)
	if err != nil {
		log.Fatal(err)
	}

	l, err := strconv.Atoi(secStr[0])
	if err != nil {
		log.Fatal(err)
	}
	var r int
	if len(secStr) == 1 {
		r = l
	} else {
		r, err = strconv.Atoi(secStr[1])
		if err != nil {
			log.Fatal(err)
		}
	}

	subval := uint32(val << r)
	submsk := ^uint32(0) << (31 - l) >> (31 - l + r) << r
	return subval, submsk
}

// isAtomic reports whether the instruction is atomic.
func isAtomic(op string) bool {
	return strings.HasPrefix(op, "AMO") || strings.HasPrefix(op, "LR_") || strings.HasPrefix(op, "SC_")
}

// isFloatReg reports whether the register of a floating point instruction is a floating point register.
func isFloatReg(op string, reg string) bool {
	switch {
	case strings.Contains(op, "FADD") || strings.Contains(op, "FSUB") ||
		strings.Contains(op, "FDIV") || strings.Contains(op, "FMUL") ||
		strings.Contains(op, "FMIN") || strings.Contains(op, "FMAX") ||
		strings.Contains(op, "FMADD") || strings.Contains(op, "FMSUB") ||
		strings.Contains(op, "FCVT_D_S") || strings.Contains(op, "FCVT_S_D") ||
		strings.Contains(op, "FCVT_D_Q") || strings.Contains(op, "FCVT_Q_D") ||
		strings.Contains(op, "FCVT_S_Q") || strings.Contains(op, "FCVT_Q_S") ||
		strings.Contains(op, "FCVT_H_S") || strings.Contains(op, "FCVT_S_H") ||
		strings.Contains(op, "FNM") || strings.Contains(op, "FNEG") ||
		strings.Contains(op, "FSQRT") || strings.Contains(op, "FSGNJ"):
		return true

	case strings.Contains(op, "FCLASS") || strings.Contains(op, "FCVT_L") ||
		strings.Contains(op, "FCVT_W") || strings.Contains(op, "FEQ") ||
		strings.Contains(op, "FLE") || strings.Contains(op, "FLT") ||
		strings.Contains(op, "FMV_X_H") || strings.Contains(op, "FMV_X_D") ||
		strings.Contains(op, "FMV_X_W"):
		return reg != "rd"

	case strings.Contains(op, "FCVT_D") || strings.Contains(op, "FCVT_S") ||
		strings.Contains(op, "FCVT_H") || strings.Contains(op, "FCVT_Q") ||
		strings.Contains(op, "FMV_H_X") || strings.Contains(op, "FMV_D_X") ||
		strings.Contains(op, "FMV_W_X"):
		return reg != "rs"

	default:
		return false
	}
}
