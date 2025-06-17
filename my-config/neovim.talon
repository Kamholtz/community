app: neovim_in_wezterm

insert:
    key i

vim normal:
    key escape

save file:
    key escape
    key colon
    insert "w"
    key enter