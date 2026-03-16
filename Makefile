# =============================================================================
# flext-tests - Test Infrastructure Library
# =============================================================================
# Shared test utilities, builders, factories, and validation for FLEXT ecosystem.
# =============================================================================

PROJECT_NAME := flext-tests
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

.DEFAULT_GOAL := help
