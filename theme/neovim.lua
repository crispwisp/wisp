-- wisp: plugin-free colorscheme, hand-set over a dark base
return {
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = function()
        vim.o.background = "dark"
        vim.cmd.colorscheme("habamax")
        local hl = function(g, o) vim.api.nvim_set_hl(0, g, o) end

        local bg, fg = "#0a0f14", "#ccdfdb"
        local glow, shimmer = "#8ef0d2", "#b3a6f0"
        local mist, dim = "#3a4750", "#11181f"

        hl("Normal", { fg = fg, bg = bg })
        hl("NormalFloat", { fg = fg, bg = dim })
        hl("FloatBorder", { fg = mist, bg = dim })
        hl("CursorLine", { bg = "#0f161d" })
        hl("CursorLineNr", { fg = glow, bold = true })
        hl("LineNr", { fg = mist })
        hl("Visual", { bg = "#1d3a33" })
        hl("Search", { fg = bg, bg = glow })
        hl("IncSearch", { fg = bg, bg = shimmer })
        hl("StatusLine", { fg = fg, bg = dim })
        hl("WinSeparator", { fg = mist })
        hl("Pmenu", { fg = fg, bg = dim })
        hl("PmenuSel", { fg = bg, bg = glow })

        hl("Comment", { fg = mist, italic = true })
        hl("String", { fg = "#7ee8b4" })
        hl("Number", { fg = "#d8d49a" })
        hl("Boolean", { fg = "#d8d49a" })
        hl("Constant", { fg = "#97ecef" })
        hl("Identifier", { fg = fg })
        hl("Function", { fg = glow })
        hl("Statement", { fg = shimmer })
        hl("Keyword", { fg = shimmer, italic = true })
        hl("Operator", { fg = "#7fdde0" })
        hl("Type", { fg = "#8ac6e3" })
        hl("Special", { fg = "#97ecef" })
        hl("PreProc", { fg = "#c7b4fa" })
        hl("Todo", { fg = bg, bg = shimmer, bold = true })
        hl("MatchParen", { fg = glow, bold = true, underline = true })

        hl("DiagnosticError", { fg = "#e06a8a" })
        hl("DiagnosticWarn", { fg = "#d8d49a" })
        hl("DiagnosticInfo", { fg = "#8ac6e3" })
        hl("DiagnosticHint", { fg = glow })
        hl("DiffAdd", { bg = "#10261d" })
        hl("DiffChange", { bg = "#10202b" })
        hl("DiffDelete", { bg = "#2b1018" })
      end,
    },
  },
}
