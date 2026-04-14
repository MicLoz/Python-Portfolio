from transform import TRANSFORM_FUNCTIONS
from pipeline_config_schema import PIPELINE_SCHEMA


# -----------------------------
# CONFIG STRUCTURE VALIDATION
# -----------------------------

def validate_pipeline_config_structure(config, schema=PIPELINE_SCHEMA):
    errors = []

    for section, rules in schema.items():

        # -------------------------
        # REQUIRED SECTION CHECK
        # -------------------------
        if rules.get("required") and section not in config:
            errors.append(f"Missing section: {section}")
            continue

        section_value = config[section]

        if not isinstance(section_value, dict):
            errors.append(f"{section} must be a dict")
            continue

        # -------------------------
        # MODE VALIDATION (extract/load)
        # -------------------------
        if "modes" in rules:

            mode = section_value.get("mode")

            if not mode:
                errors.append(f"{section} missing 'mode'")
                continue

            if mode not in rules["modes"]:
                errors.append(f"{section} has invalid mode: {mode}")
                continue

            for key in rules["modes"][mode]["required_keys"]:
                if key not in section_value:
                    errors.append(
                        f"{section} ({mode}) missing required key: {key}"
                    )

        # -------------------------
        # TRANSFORM STRUCTURE ONLY
        # -------------------------
        if section == "transform":

            steps = section_value.get("steps")

            if not isinstance(steps, list):
                errors.append("transform.steps must be a list")
                continue

            for i, step in enumerate(steps):

                if not isinstance(step, dict):
                    errors.append(f"transform.steps[{i}] must be dict")
                    continue

                op = step.get("op")

                if not op:
                    errors.append(f"transform.steps[{i}] missing 'op'")
                    continue

                if op not in TRANSFORM_FUNCTIONS:
                    errors.append(
                        f"transform.steps[{i}] invalid op: {op}. "
                        f"Allowed: {list(TRANSFORM_FUNCTIONS.keys())}"
                    )

    return errors