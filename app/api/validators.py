from marshmallow import Schema, fields, validate

class StartFlowSchema(Schema):
    phone_number = fields.Str(required=True, validate=validate.Regexp(r'^\+?1?\d{10,15}$'))
    flow_type = fields.Str(required=True, validate=validate.OneOf(['desktop', 'mobile']))
    ssn = fields.Str(required=True, validate=validate.Length(equal=4))

class ValidatePhoneNumberSchema(Schema):
    correlation_id = fields.Str(required=True)

class AddressSchema(Schema):
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    postal_code = fields.Str(required=True)

class IndividualSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    addresses = fields.List(fields.Nested(AddressSchema), required=True)
    email_addresses = fields.List(fields.Email(), required=True)
    dob = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}$'))  # YYYY-MM format
    ssn = fields.Str(required=True, validate=validate.Regexp(r'^\d{9}$'))  # 9 digits

class CompleteFlowSchema(Schema):
    individual = fields.Nested(IndividualSchema, required=True)
    correlation_id = fields.Str(required=True)