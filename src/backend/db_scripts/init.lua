box.cfg{
    listen=3301
}

local function create_user_schema()
    local space = box.schema.create_space('user')
    space:create_index('primary')
end

local function bootstrap()
    box.once('boostrap_0001', create_user_schema)
end

bootstrap()
