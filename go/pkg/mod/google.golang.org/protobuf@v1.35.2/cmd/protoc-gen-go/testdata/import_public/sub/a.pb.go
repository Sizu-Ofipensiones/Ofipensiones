// Copyright 2018 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// Code generated by protoc-gen-go. DO NOT EDIT.
// source: cmd/protoc-gen-go/testdata/import_public/sub/a.proto

package sub

import (
	sub2 "google.golang.org/protobuf/cmd/protoc-gen-go/testdata/import_public/sub2"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	math "math"
	reflect "reflect"
	sync "sync"
)

// Symbols defined in public import of cmd/protoc-gen-go/testdata/import_public/sub2/a.proto.

type Sub2Message = sub2.Sub2Message

type E int32

const (
	E_ZERO E = 0
)

// Enum value maps for E.
var (
	E_name = map[int32]string{
		0: "ZERO",
	}
	E_value = map[string]int32{
		"ZERO": 0,
	}
)

func (x E) Enum() *E {
	p := new(E)
	*p = x
	return p
}

func (x E) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (E) Descriptor() protoreflect.EnumDescriptor {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[0].Descriptor()
}

func (E) Type() protoreflect.EnumType {
	return &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[0]
}

func (x E) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Do not use.
func (x *E) UnmarshalJSON(b []byte) error {
	num, err := protoimpl.X.UnmarshalJSONEnum(x.Descriptor(), b)
	if err != nil {
		return err
	}
	*x = E(num)
	return nil
}

// Deprecated: Use E.Descriptor instead.
func (E) EnumDescriptor() ([]byte, []int) {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP(), []int{0}
}

type M_Subenum int32

const (
	M_M_ZERO M_Subenum = 0
)

// Enum value maps for M_Subenum.
var (
	M_Subenum_name = map[int32]string{
		0: "M_ZERO",
	}
	M_Subenum_value = map[string]int32{
		"M_ZERO": 0,
	}
)

func (x M_Subenum) Enum() *M_Subenum {
	p := new(M_Subenum)
	*p = x
	return p
}

func (x M_Subenum) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (M_Subenum) Descriptor() protoreflect.EnumDescriptor {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[1].Descriptor()
}

func (M_Subenum) Type() protoreflect.EnumType {
	return &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[1]
}

func (x M_Subenum) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Do not use.
func (x *M_Subenum) UnmarshalJSON(b []byte) error {
	num, err := protoimpl.X.UnmarshalJSONEnum(x.Descriptor(), b)
	if err != nil {
		return err
	}
	*x = M_Subenum(num)
	return nil
}

// Deprecated: Use M_Subenum.Descriptor instead.
func (M_Subenum) EnumDescriptor() ([]byte, []int) {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP(), []int{0, 0}
}

type M_Submessage_Submessage_Subenum int32

const (
	M_Submessage_M_SUBMESSAGE_ZERO M_Submessage_Submessage_Subenum = 0
)

// Enum value maps for M_Submessage_Submessage_Subenum.
var (
	M_Submessage_Submessage_Subenum_name = map[int32]string{
		0: "M_SUBMESSAGE_ZERO",
	}
	M_Submessage_Submessage_Subenum_value = map[string]int32{
		"M_SUBMESSAGE_ZERO": 0,
	}
)

func (x M_Submessage_Submessage_Subenum) Enum() *M_Submessage_Submessage_Subenum {
	p := new(M_Submessage_Submessage_Subenum)
	*p = x
	return p
}

func (x M_Submessage_Submessage_Subenum) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (M_Submessage_Submessage_Subenum) Descriptor() protoreflect.EnumDescriptor {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[2].Descriptor()
}

func (M_Submessage_Submessage_Subenum) Type() protoreflect.EnumType {
	return &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes[2]
}

func (x M_Submessage_Submessage_Subenum) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Do not use.
func (x *M_Submessage_Submessage_Subenum) UnmarshalJSON(b []byte) error {
	num, err := protoimpl.X.UnmarshalJSONEnum(x.Descriptor(), b)
	if err != nil {
		return err
	}
	*x = M_Submessage_Submessage_Subenum(num)
	return nil
}

// Deprecated: Use M_Submessage_Submessage_Subenum.Descriptor instead.
func (M_Submessage_Submessage_Subenum) EnumDescriptor() ([]byte, []int) {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP(), []int{0, 0, 0}
}

type M struct {
	state           protoimpl.MessageState
	sizeCache       protoimpl.SizeCache
	unknownFields   protoimpl.UnknownFields
	extensionFields protoimpl.ExtensionFields

	// Field using a type in the same Go package, but a different source file.
	M2 *M2      `protobuf:"bytes,1,opt,name=m2" json:"m2,omitempty"`
	S  *string  `protobuf:"bytes,4,opt,name=s,def=default" json:"s,omitempty"`
	B  []byte   `protobuf:"bytes,5,opt,name=b,def=default" json:"b,omitempty"`
	F  *float64 `protobuf:"fixed64,6,opt,name=f,def=nan" json:"f,omitempty"`
	// Types that are assignable to OneofField:
	//
	//	*M_OneofInt32
	//	*M_OneofInt64
	OneofField isM_OneofField `protobuf_oneof:"oneof_field"`
}

// Default values for M fields.
const (
	Default_M_S = string("default")
)

// Default values for M fields.
var (
	Default_M_B = []byte("default")
	Default_M_F = float64(math.NaN())
)

func (x *M) Reset() {
	*x = M{}
	mi := &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *M) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*M) ProtoMessage() {}

func (x *M) ProtoReflect() protoreflect.Message {
	mi := &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use M.ProtoReflect.Descriptor instead.
func (*M) Descriptor() ([]byte, []int) {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP(), []int{0}
}

func (x *M) GetM2() *M2 {
	if x != nil {
		return x.M2
	}
	return nil
}

func (x *M) GetS() string {
	if x != nil && x.S != nil {
		return *x.S
	}
	return Default_M_S
}

func (x *M) GetB() []byte {
	if x != nil && x.B != nil {
		return x.B
	}
	return append([]byte(nil), Default_M_B...)
}

func (x *M) GetF() float64 {
	if x != nil && x.F != nil {
		return *x.F
	}
	return Default_M_F
}

func (m *M) GetOneofField() isM_OneofField {
	if m != nil {
		return m.OneofField
	}
	return nil
}

func (x *M) GetOneofInt32() int32 {
	if x, ok := x.GetOneofField().(*M_OneofInt32); ok {
		return x.OneofInt32
	}
	return 0
}

func (x *M) GetOneofInt64() int64 {
	if x, ok := x.GetOneofField().(*M_OneofInt64); ok {
		return x.OneofInt64
	}
	return 0
}

type isM_OneofField interface {
	isM_OneofField()
}

type M_OneofInt32 struct {
	OneofInt32 int32 `protobuf:"varint,2,opt,name=oneof_int32,json=oneofInt32,oneof"`
}

type M_OneofInt64 struct {
	OneofInt64 int64 `protobuf:"varint,3,opt,name=oneof_int64,json=oneofInt64,oneof"`
}

func (*M_OneofInt32) isM_OneofField() {}

func (*M_OneofInt64) isM_OneofField() {}

type M_Submessage struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Types that are assignable to SubmessageOneofField:
	//
	//	*M_Submessage_SubmessageOneofInt32
	//	*M_Submessage_SubmessageOneofInt64
	SubmessageOneofField isM_Submessage_SubmessageOneofField `protobuf_oneof:"submessage_oneof_field"`
}

func (x *M_Submessage) Reset() {
	*x = M_Submessage{}
	mi := &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *M_Submessage) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*M_Submessage) ProtoMessage() {}

func (x *M_Submessage) ProtoReflect() protoreflect.Message {
	mi := &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use M_Submessage.ProtoReflect.Descriptor instead.
func (*M_Submessage) Descriptor() ([]byte, []int) {
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP(), []int{0, 0}
}

func (m *M_Submessage) GetSubmessageOneofField() isM_Submessage_SubmessageOneofField {
	if m != nil {
		return m.SubmessageOneofField
	}
	return nil
}

func (x *M_Submessage) GetSubmessageOneofInt32() int32 {
	if x, ok := x.GetSubmessageOneofField().(*M_Submessage_SubmessageOneofInt32); ok {
		return x.SubmessageOneofInt32
	}
	return 0
}

func (x *M_Submessage) GetSubmessageOneofInt64() int64 {
	if x, ok := x.GetSubmessageOneofField().(*M_Submessage_SubmessageOneofInt64); ok {
		return x.SubmessageOneofInt64
	}
	return 0
}

type isM_Submessage_SubmessageOneofField interface {
	isM_Submessage_SubmessageOneofField()
}

type M_Submessage_SubmessageOneofInt32 struct {
	SubmessageOneofInt32 int32 `protobuf:"varint,1,opt,name=submessage_oneof_int32,json=submessageOneofInt32,oneof"`
}

type M_Submessage_SubmessageOneofInt64 struct {
	SubmessageOneofInt64 int64 `protobuf:"varint,2,opt,name=submessage_oneof_int64,json=submessageOneofInt64,oneof"`
}

func (*M_Submessage_SubmessageOneofInt32) isM_Submessage_SubmessageOneofField() {}

func (*M_Submessage_SubmessageOneofInt64) isM_Submessage_SubmessageOneofField() {}

var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_extTypes = []protoimpl.ExtensionInfo{
	{
		ExtendedType:  (*M)(nil),
		ExtensionType: (*string)(nil),
		Field:         100,
		Name:          "goproto.protoc.import_public.sub.extension_field",
		Tag:           "bytes,100,opt,name=extension_field",
		Filename:      "cmd/protoc-gen-go/testdata/import_public/sub/a.proto",
	},
}

// Extension fields to M.
var (
	// optional string extension_field = 100;
	E_ExtensionField = &file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_extTypes[0]
)

var File_cmd_protoc_gen_go_testdata_import_public_sub_a_proto protoreflect.FileDescriptor

var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDesc = []byte{
	0x0a, 0x34, 0x63, 0x6d, 0x64, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x63, 0x2d, 0x67, 0x65, 0x6e,
	0x2d, 0x67, 0x6f, 0x2f, 0x74, 0x65, 0x73, 0x74, 0x64, 0x61, 0x74, 0x61, 0x2f, 0x69, 0x6d, 0x70,
	0x6f, 0x72, 0x74, 0x5f, 0x70, 0x75, 0x62, 0x6c, 0x69, 0x63, 0x2f, 0x73, 0x75, 0x62, 0x2f, 0x61,
	0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x20, 0x67, 0x6f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x63, 0x2e, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x5f, 0x70, 0x75,
	0x62, 0x6c, 0x69, 0x63, 0x2e, 0x73, 0x75, 0x62, 0x1a, 0x35, 0x63, 0x6d, 0x64, 0x2f, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x63, 0x2d, 0x67, 0x65, 0x6e, 0x2d, 0x67, 0x6f, 0x2f, 0x74, 0x65, 0x73, 0x74,
	0x64, 0x61, 0x74, 0x61, 0x2f, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x5f, 0x70, 0x75, 0x62, 0x6c,
	0x69, 0x63, 0x2f, 0x73, 0x75, 0x62, 0x32, 0x2f, 0x61, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x1a,
	0x34, 0x63, 0x6d, 0x64, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x63, 0x2d, 0x67, 0x65, 0x6e, 0x2d,
	0x67, 0x6f, 0x2f, 0x74, 0x65, 0x73, 0x74, 0x64, 0x61, 0x74, 0x61, 0x2f, 0x69, 0x6d, 0x70, 0x6f,
	0x72, 0x74, 0x5f, 0x70, 0x75, 0x62, 0x6c, 0x69, 0x63, 0x2f, 0x73, 0x75, 0x62, 0x2f, 0x62, 0x2e,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0xb6, 0x03, 0x0a, 0x01, 0x4d, 0x12, 0x34, 0x0a, 0x02, 0x6d,
	0x32, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x24, 0x2e, 0x67, 0x6f, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x63, 0x2e, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x5f,
	0x70, 0x75, 0x62, 0x6c, 0x69, 0x63, 0x2e, 0x73, 0x75, 0x62, 0x2e, 0x4d, 0x32, 0x52, 0x02, 0x6d,
	0x32, 0x12, 0x15, 0x0a, 0x01, 0x73, 0x18, 0x04, 0x20, 0x01, 0x28, 0x09, 0x3a, 0x07, 0x64, 0x65,
	0x66, 0x61, 0x75, 0x6c, 0x74, 0x52, 0x01, 0x73, 0x12, 0x15, 0x0a, 0x01, 0x62, 0x18, 0x05, 0x20,
	0x01, 0x28, 0x0c, 0x3a, 0x07, 0x64, 0x65, 0x66, 0x61, 0x75, 0x6c, 0x74, 0x52, 0x01, 0x62, 0x12,
	0x11, 0x0a, 0x01, 0x66, 0x18, 0x06, 0x20, 0x01, 0x28, 0x01, 0x3a, 0x03, 0x6e, 0x61, 0x6e, 0x52,
	0x01, 0x66, 0x12, 0x21, 0x0a, 0x0b, 0x6f, 0x6e, 0x65, 0x6f, 0x66, 0x5f, 0x69, 0x6e, 0x74, 0x33,
	0x32, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x48, 0x00, 0x52, 0x0a, 0x6f, 0x6e, 0x65, 0x6f, 0x66,
	0x49, 0x6e, 0x74, 0x33, 0x32, 0x12, 0x21, 0x0a, 0x0b, 0x6f, 0x6e, 0x65, 0x6f, 0x66, 0x5f, 0x69,
	0x6e, 0x74, 0x36, 0x34, 0x18, 0x03, 0x20, 0x01, 0x28, 0x03, 0x48, 0x00, 0x52, 0x0a, 0x6f, 0x6e,
	0x65, 0x6f, 0x66, 0x49, 0x6e, 0x74, 0x36, 0x34, 0x1a, 0xc3, 0x01, 0x0a, 0x0a, 0x53, 0x75, 0x62,
	0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x12, 0x36, 0x0a, 0x16, 0x73, 0x75, 0x62, 0x6d, 0x65,
	0x73, 0x73, 0x61, 0x67, 0x65, 0x5f, 0x6f, 0x6e, 0x65, 0x6f, 0x66, 0x5f, 0x69, 0x6e, 0x74, 0x33,
	0x32, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x48, 0x00, 0x52, 0x14, 0x73, 0x75, 0x62, 0x6d, 0x65,
	0x73, 0x73, 0x61, 0x67, 0x65, 0x4f, 0x6e, 0x65, 0x6f, 0x66, 0x49, 0x6e, 0x74, 0x33, 0x32, 0x12,
	0x36, 0x0a, 0x16, 0x73, 0x75, 0x62, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x5f, 0x6f, 0x6e,
	0x65, 0x6f, 0x66, 0x5f, 0x69, 0x6e, 0x74, 0x36, 0x34, 0x18, 0x02, 0x20, 0x01, 0x28, 0x03, 0x48,
	0x00, 0x52, 0x14, 0x73, 0x75, 0x62, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x4f, 0x6e, 0x65,
	0x6f, 0x66, 0x49, 0x6e, 0x74, 0x36, 0x34, 0x22, 0x2b, 0x0a, 0x12, 0x53, 0x75, 0x62, 0x6d, 0x65,
	0x73, 0x73, 0x61, 0x67, 0x65, 0x5f, 0x53, 0x75, 0x62, 0x65, 0x6e, 0x75, 0x6d, 0x12, 0x15, 0x0a,
	0x11, 0x4d, 0x5f, 0x53, 0x55, 0x42, 0x4d, 0x45, 0x53, 0x53, 0x41, 0x47, 0x45, 0x5f, 0x5a, 0x45,
	0x52, 0x4f, 0x10, 0x00, 0x42, 0x18, 0x0a, 0x16, 0x73, 0x75, 0x62, 0x6d, 0x65, 0x73, 0x73, 0x61,
	0x67, 0x65, 0x5f, 0x6f, 0x6e, 0x65, 0x6f, 0x66, 0x5f, 0x66, 0x69, 0x65, 0x6c, 0x64, 0x22, 0x15,
	0x0a, 0x07, 0x53, 0x75, 0x62, 0x65, 0x6e, 0x75, 0x6d, 0x12, 0x0a, 0x0a, 0x06, 0x4d, 0x5f, 0x5a,
	0x45, 0x52, 0x4f, 0x10, 0x00, 0x2a, 0x08, 0x08, 0x64, 0x10, 0x80, 0x80, 0x80, 0x80, 0x02, 0x42,
	0x0d, 0x0a, 0x0b, 0x6f, 0x6e, 0x65, 0x6f, 0x66, 0x5f, 0x66, 0x69, 0x65, 0x6c, 0x64, 0x2a, 0x0d,
	0x0a, 0x01, 0x45, 0x12, 0x08, 0x0a, 0x04, 0x5a, 0x45, 0x52, 0x4f, 0x10, 0x00, 0x3a, 0x4c, 0x0a,
	0x0f, 0x65, 0x78, 0x74, 0x65, 0x6e, 0x73, 0x69, 0x6f, 0x6e, 0x5f, 0x66, 0x69, 0x65, 0x6c, 0x64,
	0x12, 0x23, 0x2e, 0x67, 0x6f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x63, 0x2e, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x5f, 0x70, 0x75, 0x62, 0x6c, 0x69, 0x63, 0x2e,
	0x73, 0x75, 0x62, 0x2e, 0x4d, 0x18, 0x64, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0e, 0x65, 0x78, 0x74,
	0x65, 0x6e, 0x73, 0x69, 0x6f, 0x6e, 0x46, 0x69, 0x65, 0x6c, 0x64, 0x42, 0x49, 0x5a, 0x47, 0x67,
	0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x67, 0x6f, 0x6c, 0x61, 0x6e, 0x67, 0x2e, 0x6f, 0x72, 0x67,
	0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2f, 0x63, 0x6d, 0x64, 0x2f, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x63, 0x2d, 0x67, 0x65, 0x6e, 0x2d, 0x67, 0x6f, 0x2f, 0x74, 0x65, 0x73, 0x74,
	0x64, 0x61, 0x74, 0x61, 0x2f, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x5f, 0x70, 0x75, 0x62, 0x6c,
	0x69, 0x63, 0x2f, 0x73, 0x75, 0x62, 0x50, 0x00,
}

var (
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescOnce sync.Once
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescData = file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDesc
)

func file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescGZIP() []byte {
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescOnce.Do(func() {
		file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescData = protoimpl.X.CompressGZIP(file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescData)
	})
	return file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDescData
}

var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes = make([]protoimpl.EnumInfo, 3)
var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes = make([]protoimpl.MessageInfo, 2)
var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_goTypes = []any{
	(E)(0),                               // 0: goproto.protoc.import_public.sub.E
	(M_Subenum)(0),                       // 1: goproto.protoc.import_public.sub.M.Subenum
	(M_Submessage_Submessage_Subenum)(0), // 2: goproto.protoc.import_public.sub.M.Submessage.Submessage_Subenum
	(*M)(nil),                            // 3: goproto.protoc.import_public.sub.M
	(*M_Submessage)(nil),                 // 4: goproto.protoc.import_public.sub.M.Submessage
	(*M2)(nil),                           // 5: goproto.protoc.import_public.sub.M2
}
var file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_depIdxs = []int32{
	5, // 0: goproto.protoc.import_public.sub.M.m2:type_name -> goproto.protoc.import_public.sub.M2
	3, // 1: goproto.protoc.import_public.sub.extension_field:extendee -> goproto.protoc.import_public.sub.M
	2, // [2:2] is the sub-list for method output_type
	2, // [2:2] is the sub-list for method input_type
	2, // [2:2] is the sub-list for extension type_name
	1, // [1:2] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_init() }
func file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_init() {
	if File_cmd_protoc_gen_go_testdata_import_public_sub_a_proto != nil {
		return
	}
	file_cmd_protoc_gen_go_testdata_import_public_sub_b_proto_init()
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[0].OneofWrappers = []any{
		(*M_OneofInt32)(nil),
		(*M_OneofInt64)(nil),
	}
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes[1].OneofWrappers = []any{
		(*M_Submessage_SubmessageOneofInt32)(nil),
		(*M_Submessage_SubmessageOneofInt64)(nil),
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDesc,
			NumEnums:      3,
			NumMessages:   2,
			NumExtensions: 1,
			NumServices:   0,
		},
		GoTypes:           file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_goTypes,
		DependencyIndexes: file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_depIdxs,
		EnumInfos:         file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_enumTypes,
		MessageInfos:      file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_msgTypes,
		ExtensionInfos:    file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_extTypes,
	}.Build()
	File_cmd_protoc_gen_go_testdata_import_public_sub_a_proto = out.File
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_rawDesc = nil
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_goTypes = nil
	file_cmd_protoc_gen_go_testdata_import_public_sub_a_proto_depIdxs = nil
}
