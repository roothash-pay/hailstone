#!/bin/bash

# --- Color Definitions ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- Cross-platform sed compatibility ---
if [[ "$(uname)" == "Darwin" ]]; then
  SED_CMD=("sed" "-i" "")
else
  SED_CMD=("sed" "-i")
fi

# --- Error Handling Function ---
exit_if() {
  local exit_code=$1
  local msg=$2
  if [[ $exit_code -ne 0 ]]; then
    if [[ -n "$msg" ]]; then
      echo -e "${RED}[ERROR]${NC} $msg" >&2
    fi
    exit $exit_code
  fi
}

# --- Path Safety Validation ---
validate_path() {
  local path_var=$1
  if [[ -z "${!path_var}" || "${!path_var}" == "/" ]]; then
    echo -e "${RED}[ERROR]${NC} Unsafe path value for $path_var: '${!path_var}'" >&2
    exit 1
  fi
}

# --- Proto Compilation Function ---
compile_protos() {
  local proto_src_dir=$1
  local intermediate_dir=$2
  
  echo -e "${GREEN}[INFO]${NC} Finding proto files in $proto_src_dir..."
  local protofiles=$(find "$proto_src_dir" -name '*.proto') 
  exit_if $? "Failed to find proto files in $proto_src_dir"

  if [[ -z "$protofiles" ]]; then
    echo -e "${RED}[ERROR]${NC} No proto files found in $proto_src_dir" >&2
    exit 1
  fi

  echo -e "${GREEN}[INFO]${NC} Found proto files:"
  echo "$protofiles"

  echo -e "${GREEN}[INFO]${NC} Compiling Python interfaces..."
  python3 -m grpc_tools.protoc \
    -I "$PROTO_SUBMODULE_DIR" \
    --python_out="$intermediate_dir" \
    --grpc_python_out="$intermediate_dir" \
    $protofiles
  exit_if $? "Protoc compilation failed"
}

# --- Import Path Fix Function ---
fix_import_paths() {
  local dir_to_fix=$1
  echo -e "${GREEN}[INFO]${NC} Fixing import paths in $dir_to_fix..."
  
  find "$dir_to_fix" -name '*.py' -exec "${SED_CMD[@]}" \
    's/^from dapplink import/from services.savour_rpc import/g' {} \;
  exit_if $? "Failed to fix import paths"

  # Cleanup backup files on macOS if they exist
  find "$dir_to_fix" -name '*.py-e' -delete 2>/dev/null
}

# --- Main Execution ---
main() {
  # --- Configuration ---
  local PROTO_SUBMODULE_DIR="external/dapplink-proto"
  local PROTO_SRC_DIR="${PROTO_SUBMODULE_DIR}/dapplink"
  local PYTHON_INTERMEDIATE_DIR="python_build_temp"
  local PYTHON_FINAL_DIR="services/savour_rpc"

  # Check if running from project root
  if [[ ! -f ".gitmodules" ]]; then
    echo -e "${RED}[ERROR]${NC} This script must be run from the project root directory." >&2
    echo -e "Usage: cd /path/to/project/root && bash scripts/proto_compile.sh" >&2
    exit 1
  fi

  # --- Path Validation ---
  for path_var in PROTO_SUBMODULE_DIR PYTHON_INTERMEDIATE_DIR PYTHON_FINAL_DIR; do
    validate_path "$path_var"
  done

  echo -e "${GREEN}[INFO]${NC} Proto Source: $PROTO_SRC_DIR"
  echo -e "${GREEN}[INFO]${NC} Intermediate Dir: $PYTHON_INTERMEDIATE_DIR"
  echo -e "${GREEN}[INFO]${NC} Final Target Dir: $PYTHON_FINAL_DIR"

  # --- Submodule Check ---
  if [[ ! -d "$PROTO_SUBMODULE_DIR" ]] || [[ -z "$(ls -A "$PROTO_SUBMODULE_DIR")" ]]; then
    echo -e "${RED}[ERROR]${NC} Proto submodule directory '$PROTO_SUBMODULE_DIR' not found or empty." >&2
    echo -e "Please run: git submodule update --init --recursive" >&2
    exit 1
  fi

  # --- Cleanup ---
  echo -e "${GREEN}[INFO]${NC} Cleaning up intermediate directory..."
  rm -rf "$PYTHON_INTERMEDIATE_DIR"
  exit_if $? "Failed to clean up intermediate directory"

  echo -e "${GREEN}[INFO]${NC} Creating intermediate directory structure..."
  mkdir -p "$PYTHON_INTERMEDIATE_DIR"
  exit_if $? "Failed to create intermediate directory: $PYTHON_INTERMEDIATE_DIR"

  # --- Compilation ---
  compile_protos "$PROTO_SRC_DIR" "$PYTHON_INTERMEDIATE_DIR"
  local protoc_output_dir="${PYTHON_INTERMEDIATE_DIR}/dapplink"
  
  # --- Post-processing ---
  echo -e "${GREEN}[INFO]${NC} Creating __init__.py in output directory..."
  touch "${protoc_output_dir}/__init__.py"
  exit_if $? "Failed to create __init__.py"

  fix_import_paths "$protoc_output_dir"

  # --- Final Sync ---
  echo -e "${GREEN}[INFO]${NC} Syncing generated code to final destination: $PYTHON_FINAL_DIR"
  mkdir -p "$PYTHON_FINAL_DIR"
  exit_if $? "Failed to create final target directory: $PYTHON_FINAL_DIR"

  rsync -av --delete "$protoc_output_dir/" "$PYTHON_FINAL_DIR/"
  exit_if $? "Failed to sync generated code to $PYTHON_FINAL_DIR"

  # --- Finalization ---
  echo -e "${GREEN}[INFO]${NC} Cleaning up intermediate directory..."
  rm -rf "$PYTHON_INTERMEDIATE_DIR"
  exit_if $? "Failed to remove intermediate directory"

  echo -e "${GREEN}[SUCCESS]${NC} Proto compilation completed successfully!"
}

# --- Execute Main ---
main
