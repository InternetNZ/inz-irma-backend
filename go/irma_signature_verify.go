package main

import "C"

import (
	"encoding/json"
	"fmt"

	irma "github.com/privacybydesign/irmago"
)

func parse(path string) (*irma.Configuration, error) {
	conf, err := irma.NewConfiguration(path, irma.ConfigurationOptions{})

	if err != nil {
		return nil, err
	}

	err = conf.ParseFolder()
	if err != nil {
		return nil, err
	}

	return conf, nil
}

func parseSignature(signatureString string) (*irma.SignedMessage, error) {

	signature := &irma.SignedMessage{}
	signatureJSON := []byte(signatureString)
	err := json.Unmarshal(signatureJSON, signature)

	if err != nil {
		return nil, err
	}

	return signature, nil
}

func getJsonErrorString(e error) string {
	return fmt.Sprintf("{\"error\":\"%v\"}", e)
}

func verifyAndSerialize(signature *irma.SignedMessage, conf *irma.Configuration) (string, error) {
	credentialList, proofStatus, err := signature.Verify(conf, nil)

	credentialString, err := json.Marshal(credentialList)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("{\"proofStatus\": \"%v\", \"credentialList\": %v}",
		proofStatus, string(credentialString)), nil
}

//export Verify
func Verify(signatureString *C.char) *C.char {
	path := "go/irma_configuration"

	// Parse irma_configuration files
	conf, err := parse(path)
	if err != nil {
		return C.CString(getJsonErrorString(err))
	}

	signature, err := parseSignature(C.GoString(signatureString))
	if err != nil {
		return C.CString(getJsonErrorString(err))
	}

	result, err := verifyAndSerialize(signature, conf)
	return C.CString(result)
}

func main() {}
